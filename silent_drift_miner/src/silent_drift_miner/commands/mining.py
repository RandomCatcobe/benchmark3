"""Mining command implementations."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ..artifacts import ArtifactStore
from ..extractors.llm import LLMConfig, LLMRefiner, OfflineLLMFilter
from ..extractors.rules import extract_candidates
from ..schema import ArtifactType, DriftCandidate, utc_now_iso
from ..sources.github_changelog import GitHubFetcher, ReleaseDoc, split_changelog_into_sections


@dataclass
class Target:
    library: str
    owner: str
    repo: str
    ecosystem: str
    use_releases_api: bool = True
    use_changelog_file: bool = False
    max_releases: int = 30
    enabled: bool = True


def _load_yaml(path: Path) -> dict:
    """Minimal YAML loader so we don't add PyYAML as a dependency.

    Supports the simple shape used in configs/targets.yaml:
        targets:
          - library: spring-boot
            owner: spring-projects
            ...
    """
    try:
        import yaml  # type: ignore
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except ImportError:
        pass

    out: dict = {"targets": []}
    cur: Optional[dict] = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("targets:"):
            continue
        if line.lstrip().startswith("- "):
            if cur:
                out["targets"].append(cur)
            cur = {}
            kv = line.lstrip()[2:]
            if ":" in kv:
                k, v = kv.split(":", 1)
                cur[k.strip()] = _coerce(v.strip())
        elif ":" in line and cur is not None:
            k, v = line.split(":", 1)
            cur[k.strip()] = _coerce(v.strip())
    if cur:
        out["targets"].append(cur)
    return out


def _coerce(v: str):
    if v.lower() in ("true", "yes"):
        return True
    if v.lower() in ("false", "no"):
        return False
    try:
        return int(v)
    except ValueError:
        pass
    return v.strip().strip('"').strip("'")


def load_targets(config_path: Path) -> list[Target]:
    data = _load_yaml(config_path)
    out: list[Target] = []
    for item in data.get("targets", []):
        out.append(Target(
            library=item["library"],
            owner=item["owner"],
            repo=item["repo"],
            ecosystem=item.get("ecosystem", "other"),
            use_releases_api=item.get("use_releases_api", True),
            use_changelog_file=item.get("use_changelog_file", False),
            max_releases=int(item.get("max_releases", 30)),
            enabled=item.get("enabled", True),
        ))
    return out


def mine_target(target: Target, fetcher: GitHubFetcher, threshold: int) -> list[DriftCandidate]:
    """Run rule-based mining over one library; return WEAK candidates."""
    docs: list[ReleaseDoc] = []
    if target.use_releases_api:
        try:
            docs.extend(fetcher.fetch_releases(target.owner, target.repo, target.max_releases))
        except Exception as e:
            print(f"[fetch] releases API failed for {target.library}: {e}", file=sys.stderr)
    if target.use_changelog_file:
        try:
            f = fetcher.fetch_changelog_file(target.owner, target.repo)
            if f:
                docs.append(f)
        except Exception as e:
            print(f"[fetch] changelog file failed for {target.library}: {e}", file=sys.stderr)

    if not docs:
        print(f"[fetch] no documents for {target.library}", file=sys.stderr)
        return []

    now_iso = utc_now_iso()
    candidates: list[DriftCandidate] = []
    for d in docs:
        if d.source_type == "changelog_file":
            sections = list(split_changelog_into_sections(d.body))
        else:
            sections = [(d.tag or d.name, d.body)]
        for version_label, section_body in sections:
            cands = extract_candidates(
                library=target.library,
                ecosystem=target.ecosystem,
                version_label=version_label,
                section_body=section_body,
                source_url=d.html_url,
                threshold=threshold,
                retrieved_at=now_iso,
            )
            candidates.extend(cands)
    return candidates


def mine_source_file(
    library: str,
    ecosystem: str,
    source_path: Path,
    source_url: str,
    threshold: int,
) -> list[DriftCandidate]:
    body = source_path.read_text(encoding="utf-8")
    sections = list(split_changelog_into_sections(body)) or [(source_path.stem, body)]
    now_iso = utc_now_iso()
    candidates: list[DriftCandidate] = []
    for version_label, section_body in sections:
        candidates.extend(
            extract_candidates(
                library=library,
                ecosystem=ecosystem,
                version_label=version_label,
                section_body=section_body,
                source_url=source_url,
                threshold=threshold,
                retrieved_at=now_iso,
            )
        )
    return candidates


def write_candidates_jsonl(cands: list[DriftCandidate], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for c in cands:
            f.write(c.to_jsonl() + "\n")


def load_candidates_jsonl(path: Path) -> list[DriftCandidate]:
    out: list[DriftCandidate] = []
    if not path.exists():
        return out
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(DriftCandidate.from_jsonl(line))
    return out


def summarize(cands: list[DriftCandidate]) -> dict:
    cat_counter = Counter(c.category.value for c in cands)
    conf_counter = Counter(c.confidence.value for c in cands)
    by_lib = Counter(c.library for c in cands)
    by_ecosystem = Counter(c.ecosystem for c in cands)
    by_source = Counter(c.evidence[0].source_type if c.evidence else "(none)" for c in cands)
    return {
        "total": len(cands),
        "by_category": dict(cat_counter),
        "by_confidence": dict(conf_counter),
        "by_library": dict(by_lib),
        "by_ecosystem": dict(by_ecosystem),
        "by_source": dict(by_source),
    }


def candidate_dir(out_dir: Optional[str], artifact_root: Optional[str]) -> Path:
    if artifact_root is None:
        return Path(out_dir or "data/candidates")
    store = ArtifactStore(artifact_root)
    if out_dir is None:
        return store.dir_for(ArtifactType.CANDIDATE)
    return store.resolve_user_path(out_dir)


def candidate_file_arg(path: str, artifact_root: Optional[str]) -> Path:
    if artifact_root is None:
        return Path(path)
    return ArtifactStore(artifact_root).resolve_user_path(path)


def build_refiner(mode: str):
    if mode == "api":
        refiner = LLMRefiner(LLMConfig())
        if not refiner.enabled:
            print("[llm] no API key found; LLM stage will be skipped per-call")
        return refiner
    if mode == "offline":
        return OfflineLLMFilter()
    return None


def refine_candidates(refiner, candidates: list[DriftCandidate]) -> list[DriftCandidate]:
    if refiner is not None and refiner.enabled and candidates:
        kept = refiner.refine_batch(candidates)
        print(f"  precision filter: kept {len(kept)} of {len(candidates)}")
        return kept
    return candidates


def cmd_mine(args: argparse.Namespace) -> int:
    out_dir = candidate_dir(args.out_dir, args.artifact_root)
    refiner = build_refiner(args.llm_mode)

    if args.source:
        if not args.library:
            print("--library is required when --source is used", file=sys.stderr)
            return 2
        source_path = Path(args.source)
        if not source_path.exists():
            print(f"source not found: {source_path}", file=sys.stderr)
            return 2
        source_url = args.source_url or source_path.as_posix()
        print(f"\n=== mining {args.library} ({args.ecosystem}) from {source_path} ===")
        weak = mine_source_file(
            library=args.library,
            ecosystem=args.ecosystem,
            source_path=source_path,
            source_url=source_url,
            threshold=args.threshold,
        )
        print(f"  rule prescreen: {len(weak)} WEAK candidates")
        kept = refine_candidates(refiner, weak)
        out_path = candidate_file_arg(args.out, args.artifact_root) if args.out else out_dir / f"{args.library}.jsonl"
        write_candidates_jsonl(kept, out_path)
        print(f"  wrote -> {out_path}")
        print("\n=== summary ===")
        print(json.dumps(summarize(kept), indent=2, ensure_ascii=False))
        return 0

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"config not found: {config_path}", file=sys.stderr)
        return 2

    targets = load_targets(config_path)
    if args.library:
        targets = [t for t in targets if t.library == args.library]
        if not targets:
            print(f"library {args.library!r} not in config", file=sys.stderr)
            return 2
    else:
        disabled = [t.library for t in targets if not t.enabled]
        targets = [t for t in targets if t.enabled]
        if disabled:
            print(f"[config] skipping disabled targets: {', '.join(disabled)}", file=sys.stderr)

    cache_dir = Path(args.cache_dir)
    fetcher = GitHubFetcher(cache_dir=cache_dir)

    all_after: list[DriftCandidate] = []
    for t in targets:
        print(f"\n=== mining {t.library} ({t.ecosystem}) ===")
        weak = mine_target(t, fetcher, threshold=args.threshold)
        print(f"  rule prescreen: {len(weak)} WEAK candidates")
        kept = refine_candidates(refiner, weak)

        out_path = out_dir / f"{t.library}.jsonl"
        write_candidates_jsonl(kept, out_path)
        print(f"  wrote -> {out_path}")
        all_after.extend(kept)

    s = summarize(all_after)
    print("\n=== summary ===")
    print(json.dumps(s, indent=2, ensure_ascii=False))
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    all_c: list[DriftCandidate] = []
    paths = args.paths or []
    if not paths:
        paths = [str(candidate_dir(args.out_dir, args.artifact_root))]
    for raw_path in paths:
        path = candidate_file_arg(raw_path, args.artifact_root) if args.artifact_root else Path(raw_path)
        if path.is_dir():
            for p in sorted(path.glob("*.jsonl")):
                all_c.extend(load_candidates_jsonl(p))
        else:
            all_c.extend(load_candidates_jsonl(path))
    s = summarize(all_c)
    print(json.dumps(s, indent=2, ensure_ascii=False))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    path = Path(args.path)
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 2

    errors: list[str] = []
    seen_ids: set[str] = set()
    total = 0
    with path.open("r", encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            raw = raw.strip()
            if not raw:
                continue
            total += 1
            try:
                c = DriftCandidate.from_jsonl(raw)
            except Exception as e:
                errors.append(f"line {lineno}: parse error — {e}")
                continue
            if c.candidate_id in seen_ids:
                errors.append(f"line {lineno}: duplicate candidate_id {c.candidate_id!r}")
            seen_ids.add(c.candidate_id)
            if not c.library:
                errors.append(f"line {lineno}: missing library")
            if not c.title:
                errors.append(f"line {lineno}: missing title")
            try:
                rt = DriftCandidate.from_jsonl(c.to_jsonl())
                if rt.candidate_id != c.candidate_id:
                    errors.append(f"line {lineno}: round-trip id mismatch")
            except Exception as e:
                errors.append(f"line {lineno}: round-trip error — {e}")

    if errors:
        for msg in errors:
            print(f"ERROR {msg}", file=sys.stderr)
        print(f"\n{len(errors)} error(s) in {total} candidates — {path}", file=sys.stderr)
        return 1

    print(f"OK — {total} candidates validated in {path}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    target = Path(args.target)
    if target.suffix == ".jsonl" or target.exists():
        path = candidate_file_arg(args.target, args.artifact_root) if args.artifact_root else target
    else:
        out_dir = candidate_dir(args.out_dir, args.artifact_root)
        path = out_dir / f"{args.target}.jsonl"
    cands = load_candidates_jsonl(path)
    if args.candidate_id:
        cands = [c for c in cands if c.candidate_id == args.candidate_id]
    if args.only_category:
        cands = [c for c in cands if c.category.value == args.only_category]
    if args.min_confidence:
        order = {"weak": 0, "uncertain_silence": 1, "high": 2}
        threshold = order[args.min_confidence]
        cands = [c for c in cands if order[c.confidence.value] >= threshold]
    cands = cands[: args.limit]
    for c in cands:
        print("─" * 80)
        print(f"[{c.confidence.value}/{c.category.value}] {c.library} {c.version_new}")
        print(f"  title: {c.title}")
        if c.summary_paraphrased:
            print(f"  summary: {c.summary_paraphrased}")
        if c.api_surface:
            print(f"  api: {', '.join(c.api_surface)}")
        if c.why_flagged:
            print(f"  rules: {', '.join(c.why_flagged)}")
        if c.evidence:
            print(f"  url: {c.evidence[0].url}")
    print("─" * 80)
    print(f"total shown: {len(cands)}")
    return 0
