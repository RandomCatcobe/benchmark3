"""SilentDriftBench eval-pack assembly for case-bank source packages."""
from __future__ import annotations

import json
import re
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .index import discover_cases
from .validation import validate_cases

POSITIVE_STATUS = "verified_keep"
HARD_NEGATIVE_STATUS = "rejected_no_diff"
DEFAULT_INCLUDED_STATUSES = (POSITIVE_STATUS,)
SPLIT_NAMES = ("train", "dev", "validation", "hidden_test", "stress_test")
ALLOWLISTED_PUBLIC_ORACLE_FIELDS = (
    "metadata.case_id",
    "metadata.track",
    "metadata.language",
    "metadata.languages",
    "metadata.ecosystem",
    "metadata.ecosystems",
    "metadata.dependency",
    "metadata.old_version",
    "metadata.new_version",
    "metadata.upstream",
    "metadata.context_condition",
    "metadata.primary_scenario",
    "metadata.application_scenarios",
    "metadata.api_surfaces",
    "metadata.cluster_key",
    "probe_outputs.old.exit_code",
    "probe_outputs.old.stderr",
    "probe_outputs.old.stdout",
    "probe_outputs.new.exit_code",
    "probe_outputs.new.stderr",
    "probe_outputs.new.stdout",
)
BASELINE_FALLBACK = {
    "context_condition": "A0_no_context",
    "probe_outputs": (
        "best_effort_existing_artifacts; generated only when source case probe_outputs, "
        "metadata provenance stdout, local data/verification result stdout, or public "
        "probe-output-overrides entries are available"
    ),
    "docs_corpus": "not generated in v1.2 quick reliable pack; downstream should treat docs baselines as absent",
}
EVAL_PACK_STRIPPED_NAMES = {
    ".pytest_cache",
    ".repro_venvs",
    ".uv-cache",
    ".uv-python",
    "__pycache__",
    "bin",
    "build",
    "dist",
    "hidden",
    "node_modules",
    "obj",
    "oracle.md",
    "target",
    "vendor",
    "expected.json",
}
MITIGATION_VALUES = {"pin", "adapt", "compat_layer", "update_tests", "monitor", "unknown"}
TEXT_EXTENSIONS = {
    ".cs",
    ".go",
    ".java",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".php",
    ".pom",
    ".properties",
    ".py",
    ".rb",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}


@dataclass(frozen=True)
class EvalCaseRecord:
    case_id: str
    source_dir: Path
    status: str
    track: str
    split: str
    cluster_key: str
    dependency: str
    upstream: dict[str, str]
    languages: tuple[str, ...]
    ecosystems: tuple[str, ...]
    public_dir: str
    hidden_dir: str
    probe_outputs_available: bool
    docs_corpus_available: bool
    public_tests_available: bool


def build_eval_pack(
    src_root: Path,
    out_root: Path,
    *,
    source_bundle_label: str | None = None,
    hard_negative_case_ids: set[str] | None = None,
    hard_negative_limit: int = 0,
) -> Path:
    """Build a solver-public/grader-hidden SilentDriftBench eval pack."""
    src_root = src_root.resolve()
    if not src_root.exists():
        raise ValueError(f"case bank source not found: {src_root}")
    if not src_root.is_dir():
        raise ValueError(f"case bank source must be a directory: {src_root}")
    if out_root.exists() and any(out_root.iterdir()):
        raise ValueError(f"eval-pack output already exists and is not empty: {out_root}")
    if hard_negative_limit < 0:
        raise ValueError("hard_negative_limit must be >= 0")

    source_validation = validate_cases(src_root)
    if source_validation.findings:
        raise ValueError("source validation failed: " + "; ".join(source_validation.findings))

    discovered_cases = discover_cases(src_root)
    selected_cases, excluded_statuses = _select_cases(
        discovered_cases,
        hard_negative_case_ids or set(),
        hard_negative_limit,
    )
    split_plan = _assign_splits(selected_cases)

    public_root = out_root / "public"
    hidden_root = out_root / "grader" / "hidden"
    public_root.mkdir(parents=True, exist_ok=True)
    hidden_root.mkdir(parents=True, exist_ok=True)

    records: list[EvalCaseRecord] = []
    for metadata in selected_cases:
        source_dir = metadata["_path"]
        case_id = metadata["case_id"]
        dependency = _infer_dependency(metadata)
        upstream = _upstream(metadata, dependency)
        cluster_key = _cluster_key(metadata, dependency)
        split = split_plan[cluster_key]
        track = _track_for_status(metadata["status"])
        public_dir = public_root / case_id
        hidden_dir = hidden_root / case_id

        public_dir.mkdir(parents=True, exist_ok=True)
        hidden_dir.mkdir(parents=True, exist_ok=True)

        _write_public_metadata(public_dir / "metadata.json", metadata, dependency, track, cluster_key, upstream)
        (public_dir / "task.md").write_text(_render_public_task(metadata, dependency), encoding="utf-8")
        shutil.copy2(source_dir / "env.md", public_dir / "env.md")
        _copy_public_tree(source_dir / "client", public_dir / "client")

        public_tests_available = _copy_optional_file(source_dir / "public_tests.json", public_dir / "public_tests.json")
        probe_outputs_available = _copy_or_derive_probe_outputs(metadata, source_dir, public_dir)
        docs_corpus_available = _copy_optional_dir(source_dir / "docs_corpus", public_dir / "docs_corpus")

        expected = _build_expected(metadata, dependency)
        (hidden_dir / "expected.json").write_text(
            json.dumps(expected, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        shutil.copy2(source_dir / "case.md", hidden_dir / "source_case.md")
        shutil.copy2(source_dir / "evidence.md", hidden_dir / "source_evidence.md")

        records.append(
            EvalCaseRecord(
                case_id=case_id,
                source_dir=source_dir,
                status=metadata["status"],
                track=track,
                split=split,
                cluster_key=cluster_key,
                dependency=dependency,
                upstream=upstream,
                languages=tuple(metadata["languages"]),
                ecosystems=tuple(metadata["ecosystems"]),
                public_dir=f"public/{case_id}",
                hidden_dir=f"grader/hidden/{case_id}",
                probe_outputs_available=probe_outputs_available,
                docs_corpus_available=docs_corpus_available,
                public_tests_available=public_tests_available,
            )
        )

    split_manifest = _build_split_manifest(records)
    (out_root / "split_manifest.json").write_text(
        json.dumps(split_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    leak_scan = scan_eval_pack_for_leaks(out_root)
    manifest = _build_manifest(
        src_root,
        source_bundle_label,
        discovered_cases,
        records,
        excluded_statuses,
        leak_scan,
    )
    (out_root / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    if leak_scan["finding_count"]:
        raise ValueError("leak scan failed: " + "; ".join(leak_scan["findings"][:5]))
    return out_root


def scan_eval_pack_for_leaks(pack_root: Path) -> dict[str, Any]:
    """Scan public payloads for hidden oracle files and direct expected-output leaks."""
    public_root = pack_root / "public"
    hidden_root = pack_root / "grader" / "hidden"
    findings: list[str] = []
    structural_count = 0
    content_count = 0
    public_file_count = 0

    if not public_root.is_dir():
        return {
            "status": "fail",
            "public_file_count": 0,
            "structural_findings": 1,
            "content_findings": 0,
            "finding_count": 1,
            "findings": [f"missing public root: {public_root}"],
        }

    for path in public_root.rglob("*"):
        if path.is_file():
            public_file_count += 1
        lowered_parts = {part.lower() for part in path.parts}
        if "hidden" in lowered_parts or path.name in {"expected.json", "oracle.md", "source_case.md", "source_evidence.md"}:
            structural_count += 1
            findings.append(f"structural hidden leak: {_as_posix(path)}")

    for case_public in sorted(child for child in public_root.iterdir() if child.is_dir()):
        case_hidden = hidden_root / case_public.name
        if not case_hidden.exists():
            continue
        public_text = _read_public_text(case_public)
        normalized_public_text = _normalize_text(public_text)
        expected_path = case_hidden / "expected.json"
        if expected_path.is_file():
            expected_text = expected_path.read_text(encoding="utf-8")
            if _normalize_text(expected_text) and _normalize_text(expected_text) in normalized_public_text:
                content_count += 1
                findings.append(f"expected.json content leaked in public/{case_public.name}")
            expected = json.loads(expected_text)
            changed_behavior = str(expected.get("changed_behavior", ""))
            if len(changed_behavior) >= 24 and _normalize_text(changed_behavior) in normalized_public_text:
                content_count += 1
                findings.append(f"changed_behavior leaked in public/{case_public.name}")

        for source_name in ("source_case.md", "source_evidence.md"):
            source_path = case_hidden / source_name
            if not source_path.is_file():
                continue
            for section in _old_new_sections(source_path.read_text(encoding="utf-8")):
                if len(section) >= 24 and _normalize_text(section) in normalized_public_text:
                    content_count += 1
                    findings.append(f"{source_name} old/new section leaked in public/{case_public.name}")

    return {
        "status": "pass" if not findings else "fail",
        "public_file_count": public_file_count,
        "structural_findings": structural_count,
        "content_findings": content_count,
        "finding_count": len(findings),
        "findings": findings[:50],
    }


def _select_cases(
    discovered_cases: list[dict[str, Any]],
    hard_negative_case_ids: set[str],
    hard_negative_limit: int,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    by_id = {case["case_id"]: case for case in discovered_cases}
    missing_ids = sorted(hard_negative_case_ids - set(by_id))
    if missing_ids:
        raise ValueError(f"unknown hard negative case_id(s): {', '.join(missing_ids)}")

    selected: list[dict[str, Any]] = []
    rejected_no_diff = [case for case in discovered_cases if case["status"] == HARD_NEGATIVE_STATUS]
    limit_ids = {case["case_id"] for case in rejected_no_diff[:hard_negative_limit]}
    requested_negative_ids = hard_negative_case_ids | limit_ids

    for case_id in sorted(requested_negative_ids):
        case = by_id[case_id]
        if case["status"] != HARD_NEGATIVE_STATUS:
            raise ValueError(f"hard negative {case_id} has status {case['status']!r}, expected {HARD_NEGATIVE_STATUS!r}")

    excluded = Counter(case["status"] for case in discovered_cases)
    for case in discovered_cases:
        if case["status"] == POSITIVE_STATUS or case["case_id"] in requested_negative_ids:
            selected.append(case)
            excluded[case["status"]] -= 1

    return selected, {status: count for status, count in sorted(excluded.items()) if count > 0}


def _assign_splits(cases: list[dict[str, Any]]) -> dict[str, str]:
    clusters: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for metadata in cases:
        dependency = _infer_dependency(metadata)
        clusters[_cluster_key(metadata, dependency)].append(metadata)

    split_targets = {
        "train": 0.55,
        "dev": 0.10,
        "validation": 0.15,
        "hidden_test": 0.15,
        "stress_test": 0.05,
    }
    split_counts = {split: 0 for split in split_targets}
    cluster_to_split: dict[str, str] = {}
    total_cases = max(1, sum(len(items) for items in clusters.values()))
    sorted_clusters = sorted(clusters.items(), key=lambda item: (-len(item[1]), item[0]))

    for cluster_key, items in sorted_clusters:
        size = len(items)
        if not cluster_to_split and size >= 2:
            split = "stress_test"
        else:
            split = max(
                split_targets,
                key=lambda name: (split_targets[name] * total_cases - split_counts[name], name),
            )
        cluster_to_split[cluster_key] = split
        split_counts[split] += size

    return cluster_to_split


def _build_split_manifest(records: list[EvalCaseRecord]) -> dict[str, Any]:
    split_names = list(SPLIT_NAMES)
    records_by_split: dict[str, list[dict[str, Any]]] = {split: [] for split in split_names}
    cluster_to_split: dict[str, str] = {}
    cluster_cases: dict[str, list[str]] = defaultdict(list)
    language_stats: dict[str, Counter[str]] = {split: Counter() for split in split_names}
    warnings: list[str] = []

    for record in records:
        records_by_split[record.split].append(_split_case_record(record))
        cluster_cases[record.cluster_key].append(record.case_id)
        previous_split = cluster_to_split.setdefault(record.cluster_key, record.split)
        if previous_split != record.split:
            warnings.append(f"cluster {record.cluster_key} crosses splits: {previous_split}, {record.split}")
        for language in record.languages:
            language_stats[record.split][language] += 1

    clusters = {
        cluster: {
            "split": cluster_to_split[cluster],
            "case_count": len(case_ids),
            "case_ids": sorted(case_ids),
        }
        for cluster, case_ids in sorted(cluster_cases.items())
    }
    split_case_counts = {split: len(records_by_split[split]) for split in split_names}
    return {
        "version": 1,
        "split_names": split_names,
        "splits": {
            split: sorted(case_records, key=lambda item: item["case_id"])
            for split, case_records in records_by_split.items()
        },
        "cluster_stats": {
            "cluster_count": len(clusters),
            "split_case_counts": split_case_counts,
            "clusters": clusters,
        },
        "language_stats": {
            split: dict(sorted(counter.items()))
            for split, counter in language_stats.items()
        },
        "warnings": warnings,
    }


def _build_manifest(
    src_root: Path,
    source_bundle_label: str | None,
    discovered_cases: list[dict[str, Any]],
    records: list[EvalCaseRecord],
    excluded_statuses: dict[str, int],
    leak_scan: dict[str, Any],
) -> dict[str, Any]:
    included_statuses = Counter(record.status for record in records)
    discovered_statuses = Counter(case["status"] for case in discovered_cases)
    return {
        "schema_version": 1,
        "source_bundle": source_bundle_label or _display_path(src_root),
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "case_count": len(records),
        "included_statuses": dict(sorted(included_statuses.items())),
        "excluded_statuses": excluded_statuses,
        "source_status_counts": dict(sorted(discovered_statuses.items())),
        "cases": [
            {
                "case_id": record.case_id,
                "source_status": record.status,
                "track": record.track,
                "split": record.split,
                "cluster_key": record.cluster_key,
                "public_dir": record.public_dir,
                "hidden_dir": record.hidden_dir,
                "probe_outputs_available": record.probe_outputs_available,
                "docs_corpus_available": record.docs_corpus_available,
                "public_tests_available": record.public_tests_available,
            }
            for record in sorted(records, key=lambda item: item.case_id)
        ],
        "probe_outputs_available": any(record.probe_outputs_available for record in records),
        "docs_corpus_available": any(record.docs_corpus_available for record in records),
        "leak_scan": leak_scan,
        "allowlisted_public_oracle_fields": list(ALLOWLISTED_PUBLIC_ORACLE_FIELDS),
        "baseline_fallback": BASELINE_FALLBACK,
    }


def _write_public_metadata(
    path: Path,
    metadata: dict[str, Any],
    dependency: str,
    track: str,
    cluster_key: str,
    upstream: dict[str, str],
) -> None:
    ecosystems = list(metadata["ecosystems"])
    languages = list(metadata["languages"])
    public_metadata = {
        "case_id": metadata["case_id"],
        "slug": metadata["slug"],
        "track": track,
        "language": languages[0] if languages else "unknown",
        "languages": languages,
        "ecosystem": ecosystems[0] if ecosystems else "unknown",
        "ecosystems": ecosystems,
        "dependency": dependency,
        "old_version": metadata["old_version"],
        "new_version": metadata["new_version"],
        "upstream": upstream,
        "context_condition": "A0_no_context",
        "primary_scenario": metadata["primary_scenario"],
        "application_scenarios": metadata["application_scenarios"],
        "api_surfaces": metadata["api_surfaces"],
        "cluster_key": cluster_key,
    }
    if metadata["status"] == HARD_NEGATIVE_STATUS:
        public_metadata["negative"] = _negative_schema(metadata, dependency)
    path.write_text(json.dumps(public_metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _render_public_task(metadata: dict[str, Any], dependency: str) -> str:
    return "\n".join(
        [
            f"# {metadata['case_id']}: SilentDrift Evaluation Task",
            "",
            "You are given a minimal client and environment notes for a dependency upgrade.",
            "Determine whether the same client behavior is stable across the version boundary.",
            "",
            "## Upgrade Boundary",
            "",
            f"- Dependency: `{dependency}`",
            f"- Old version: `{metadata['old_version']}`",
            f"- New version: `{metadata['new_version']}`",
            "",
            "## What To Do",
            "",
            "Inspect `env.md` and the `client/` files, run the probe if your environment supports it, and submit a concise diagnosis.",
            "Do not assume a drift exists; classify the case from the observable behavior.",
            "",
            "## Diagnosis Fields",
            "",
            "- `has_silent_drift`",
            "- `root_dependency`",
            "- `old_version`",
            "- `new_version`",
            "- `changed_behavior`",
            "- `affected_output_fields`",
            "- `recommended_mitigation`",
            "",
        ]
    )


def _build_expected(metadata: dict[str, Any], dependency: str) -> dict[str, Any]:
    status = metadata["status"]
    source_expected_path = metadata["_path"] / "hidden" / "expected.json"
    assertions: list[dict[str, Any]] = []
    if source_expected_path.is_file():
        assertions = json.loads(source_expected_path.read_text(encoding="utf-8")).get("assertions", [])

    has_silent_drift = status == POSITIVE_STATUS
    fields = [str(assertion.get("field")) for assertion in assertions if assertion.get("field")]
    changed_behavior = _changed_behavior(assertions, has_silent_drift)
    expected = {
        "schema_version": 1,
        "case_id": metadata["case_id"],
        "has_silent_drift": has_silent_drift,
        "root_dependency": dependency,
        "root_dependency_aliases": _dependency_aliases(metadata, dependency),
        "old_version": metadata["old_version"],
        "new_version": metadata["new_version"],
        "changed_behavior": changed_behavior,
        "affected_output_fields": fields,
        "evidence_keywords": _evidence_keywords(metadata, dependency, fields),
        "recommended_mitigation": _recommended_mitigation(metadata),
        "assertions": assertions,
    }
    if status == HARD_NEGATIVE_STATUS:
        expected["negative"] = _negative_schema(metadata, dependency)
    return expected


def _negative_schema(metadata: dict[str, Any], dependency: str) -> dict[str, str]:
    return {
        "case_id": metadata["case_id"],
        "negative_type": "upgrade_no_drift",
        "ecosystem": metadata["ecosystems"][0] if metadata["ecosystems"] else "unknown",
        "dependency": dependency,
        "old_version": metadata["old_version"],
        "new_version": metadata["new_version"],
        "public_symptom": metadata["title"],
        "expected_label": "no_silent_drift",
        "confounder": "Both versions execute without a grader-approved behavior delta.",
        "grading_notes": "Hard negative selected explicitly from rejected_no_diff source status.",
    }


def _changed_behavior(assertions: list[dict[str, Any]], has_silent_drift: bool) -> str:
    if not has_silent_drift:
        return "No grader-approved silent behavior drift."
    names = [str(assertion["name"]) for assertion in assertions if assertion.get("name")]
    if names:
        return "; ".join(names)
    return "Observable output differs across the dependency version boundary."


def _copy_public_tree(source: Path, destination: Path) -> None:
    if not source.is_dir():
        raise ValueError(f"case is missing client/: {source}")
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(*EVAL_PACK_STRIPPED_NAMES),
    )


def _copy_optional_dir(source: Path, destination: Path) -> bool:
    if not source.is_dir():
        return False
    _copy_public_tree(source, destination)
    return True


def _copy_optional_file(source: Path, destination: Path) -> bool:
    if not source.is_file():
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return True


def _copy_or_derive_probe_outputs(metadata: dict[str, Any], source_dir: Path, public_dir: Path) -> bool:
    source_probe_dir = source_dir / "probe_outputs"
    old_path = source_probe_dir / "old.json"
    new_path = source_probe_dir / "new.json"
    if old_path.is_file() and new_path.is_file():
        for path in (old_path, new_path):
            json.loads(path.read_text(encoding="utf-8"))
        destination = public_dir / "probe_outputs"
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copy2(old_path, destination / "old.json")
        shutil.copy2(new_path, destination / "new.json")
        return True

    derived = _derive_probe_outputs(metadata, source_dir)
    if derived is None:
        return False
    destination = public_dir / "probe_outputs"
    destination.mkdir(parents=True, exist_ok=True)
    for label in ("old", "new"):
        (destination / f"{label}.json").write_text(
            json.dumps(derived[label], indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    return True


def _derive_probe_outputs(metadata: dict[str, Any], source_dir: Path) -> dict[str, dict[str, Any]] | None:
    from_provenance = _probe_outputs_from_provenance(metadata)
    if from_provenance is not None:
        return from_provenance
    from_reproduction_result = _probe_outputs_from_reproduction_result(metadata)
    if from_reproduction_result is not None:
        return from_reproduction_result
    return _probe_outputs_from_overrides(metadata, source_dir)


def _probe_outputs_from_provenance(metadata: dict[str, Any]) -> dict[str, dict[str, Any]] | None:
    provenance = metadata.get("provenance", {})
    if "old_stdout" not in provenance or "new_stdout" not in provenance:
        return None
    return {
        "old": _probe_payload(
            metadata,
            "old",
            provenance.get("old_stdout", ""),
            provenance.get("old_stderr", ""),
            provenance.get("old_exit", 0),
            "metadata.provenance",
        ),
        "new": _probe_payload(
            metadata,
            "new",
            provenance.get("new_stdout", ""),
            provenance.get("new_stderr", ""),
            provenance.get("new_exit", 0),
            "metadata.provenance",
        ),
    }


def _probe_outputs_from_reproduction_result(metadata: dict[str, Any]) -> dict[str, dict[str, Any]] | None:
    result_path = _resolve_reproduction_result_path(metadata)
    if result_path is None:
        return None
    try:
        result = json.loads(result_path.read_text(encoding="utf-8"))
    except Exception:
        return None

    old_run = result.get("old_run", {})
    new_run = result.get("new_run", {})
    old_stdout = _read_run_text(old_run.get("stdout_path"))
    new_stdout = _read_run_text(new_run.get("stdout_path"))
    if old_stdout is None or new_stdout is None:
        return None
    return {
        "old": _probe_payload(
            metadata,
            "old",
            old_stdout,
            _read_run_text(old_run.get("stderr_path")) or "",
            old_run.get("exit_code", 0),
            _display_path(result_path),
        ),
        "new": _probe_payload(
            metadata,
            "new",
            new_stdout,
            _read_run_text(new_run.get("stderr_path")) or "",
            new_run.get("exit_code", 0),
            _display_path(result_path),
        ),
    }


def _probe_outputs_from_overrides(metadata: dict[str, Any], source_dir: Path) -> dict[str, dict[str, Any]] | None:
    overrides_path = _probe_output_overrides_path(source_dir)
    if overrides_path is None:
        return None
    try:
        overrides = json.loads(overrides_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    entry = overrides.get("cases", {}).get(metadata["case_id"])
    if not isinstance(entry, dict):
        return None
    old_entry = entry.get("old", {})
    new_entry = entry.get("new", {})
    if not isinstance(old_entry, dict) or not isinstance(new_entry, dict):
        return None
    if "stdout" not in old_entry or "stdout" not in new_entry:
        return None
    default_source = entry.get("source") or overrides.get("source") or _display_path(overrides_path)
    return {
        "old": _probe_payload(
            metadata,
            "old",
            old_entry.get("stdout", ""),
            old_entry.get("stderr", ""),
            old_entry.get("exit_code", 0),
            old_entry.get("source") or default_source,
        ),
        "new": _probe_payload(
            metadata,
            "new",
            new_entry.get("stdout", ""),
            new_entry.get("stderr", ""),
            new_entry.get("exit_code", 0),
            new_entry.get("source") or default_source,
        ),
    }


def _probe_output_overrides_path(source_dir: Path) -> Path | None:
    for parent in (source_dir, *source_dir.parents):
        candidate = parent / "probe-output-overrides.json"
        if candidate.is_file():
            return candidate
    return None


def _resolve_reproduction_result_path(metadata: dict[str, Any]) -> Path | None:
    raw_path = metadata.get("provenance", {}).get("reproduction_result")
    if not isinstance(raw_path, str) or not raw_path:
        return None
    path = Path(raw_path)
    if not path.is_absolute():
        path = Path.cwd() / path
    if path.is_file() and path.suffix.lower() == ".json":
        return path
    if not path.is_dir():
        return None
    result_paths = sorted(path.rglob("result.json"), key=lambda item: item.as_posix(), reverse=True)
    if not result_paths:
        return None
    return result_paths[0]


def _read_run_text(raw_path: Any) -> str | None:
    if not isinstance(raw_path, str) or not raw_path:
        return None
    path = Path(raw_path)
    if not path.is_absolute():
        path = Path.cwd() / path
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8").rstrip("\n")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace").rstrip("\n")


def _probe_payload(
    metadata: dict[str, Any],
    label: str,
    stdout: Any,
    stderr: Any,
    exit_code: Any,
    source: str,
) -> dict[str, Any]:
    stdout_text = "" if stdout is None else str(stdout)
    stderr_text = "" if stderr is None else str(stderr)
    return {
        "case_id": metadata["case_id"],
        "label": label,
        "version": metadata["old_version"] if label == "old" else metadata["new_version"],
        "exit_code": _safe_int(exit_code, default=0),
        "stdout": _structured_text(stdout_text),
        "stderr": _structured_text(stderr_text),
        "source": source,
    }


def _structured_text(value: str) -> dict[str, Any]:
    payload: dict[str, Any] = {"raw": value}
    stripped = value.strip()
    if not stripped:
        payload["parsed_json"] = None
        return payload
    try:
        payload["parsed_json"] = json.loads(stripped)
    except json.JSONDecodeError:
        payload["parsed_json"] = None
    return payload


def _safe_int(value: Any, *, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _split_case_record(record: EvalCaseRecord) -> dict[str, Any]:
    return {
        "case_id": record.case_id,
        "cluster_key": record.cluster_key,
        "language": record.languages[0] if record.languages else "unknown",
        "track": record.track,
        "upstream": record.upstream,
    }


def _upstream(metadata: dict[str, Any], dependency: str) -> dict[str, str]:
    ecosystems = list(metadata["ecosystems"])
    return {
        "ecosystem": ecosystems[0] if ecosystems else "unknown",
        "package": dependency,
        "name": dependency,
        "version": f"{metadata['old_version']}->{metadata['new_version']}",
    }


def _track_for_status(status: str) -> str:
    if status == HARD_NEGATIVE_STATUS:
        return "HardNegative"
    return "OfflineDependencyDrift"


def _cluster_key(metadata: dict[str, Any], dependency: str) -> str:
    ecosystem = metadata["ecosystems"][0] if metadata["ecosystems"] else "unknown"
    return f"{ecosystem}:{_normalize_dependency(dependency)}"


def _infer_dependency(metadata: dict[str, Any]) -> str:
    old_name = _strip_version_suffix(metadata["old_version"])
    new_name = _strip_version_suffix(metadata["new_version"])
    if old_name and new_name and _normalize_dependency(old_name) == _normalize_dependency(new_name):
        return old_name
    if old_name and not _looks_version_only(old_name):
        return old_name
    if new_name and not _looks_version_only(new_name):
        return new_name
    return _title_dependency(metadata["title"])


def _strip_version_suffix(value: str) -> str:
    tokens = value.replace("->", " ").split()
    while tokens and _looks_version_token(tokens[-1]):
        tokens.pop()
    return " ".join(tokens).strip()


def _looks_version_only(value: str) -> bool:
    return bool(re.fullmatch(r"[vV]?\d[\w.+\-*xX<>=, ]*", value.strip()))


def _looks_version_token(token: str) -> bool:
    token = token.strip("()[]{}:,")
    if token.lower() in {"x", "latest"}:
        return True
    return bool(re.fullmatch(r"[vV]?\d[\w.+\-*xX<>=,]*", token))


def _title_dependency(title: str) -> str:
    stop_words = {
        "adds",
        "allows",
        "becomes",
        "changes",
        "detects",
        "defaults",
        "deserializes",
        "emits",
        "encodes",
        "infers",
        "inserts",
        "matches",
        "no",
        "normalizes",
        "orders",
        "recognizes",
        "removes",
        "returns",
        "starts",
        "stops",
        "treats",
    }
    words = title.split()
    if words and words[0].lower() == "old15":
        words = words[1:]
    selected: list[str] = []
    for word in words:
        cleaned = re.sub(r"[^A-Za-z0-9_.:+-]", "", word).lower()
        if selected and _looks_version_token(cleaned):
            continue
        if cleaned in stop_words:
            break
        selected.append(word.strip(" ,:;"))
        if len(selected) >= 4:
            break
    return " ".join(selected).strip() or "unknown"


def _normalize_dependency(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized or "unknown"


def _dependency_aliases(metadata: dict[str, Any], dependency: str) -> list[str]:
    aliases = {
        dependency,
        dependency.lower(),
        _normalize_dependency(dependency),
    }
    if ":" in dependency:
        aliases.add(dependency.split(":")[-1])
    title_dependency = _title_dependency(metadata["title"])
    if title_dependency != dependency:
        aliases.add(title_dependency)
    return sorted(alias for alias in aliases if alias)


def _evidence_keywords(metadata: dict[str, Any], dependency: str, fields: list[str]) -> list[str]:
    values = [dependency, *_dependency_aliases(metadata, dependency)]
    values.extend(fields)
    values.extend(metadata["drift_patterns"])
    values.extend(metadata["failure_modes"])
    values.extend(_version_keywords(metadata["old_version"]))
    values.extend(_version_keywords(metadata["new_version"]))
    deduped: dict[str, str] = {}
    for value in values:
        if not value:
            continue
        key = value.lower()
        deduped.setdefault(key, value)
    return list(deduped.values())[:20]


def _version_keywords(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"[\s,>]+", value) if part.strip() and not _looks_version_token(part)]


def _recommended_mitigation(metadata: dict[str, Any]) -> str:
    patterns = set(metadata["drift_patterns"])
    failure_modes = set(metadata["failure_modes"])
    if "field-removed-or-masked" in patterns:
        return "compat_layer"
    if "bundled-data-changed" in patterns or "runtime-locale-changed" in patterns:
        return "monitor"
    if "validation-relaxed" in patterns or "validation-strictness-increased" in patterns:
        return "update_tests"
    if "success-but-no-effect" in patterns or "missing-field" in failure_modes:
        return "monitor"
    mitigation = "adapt" if patterns else "unknown"
    if mitigation not in MITIGATION_VALUES:
        return "unknown"
    return mitigation


def _read_public_text(case_public: Path) -> str:
    chunks: list[str] = []
    for path in sorted(case_public.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            chunks.append(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            continue
    return "\n".join(chunks)


def _old_new_sections(text: str) -> list[str]:
    sections: list[str] = []
    matches = list(re.finditer(r"^##\s+(Old|New) Behavior\s*$", text, flags=re.MULTILINE | re.IGNORECASE))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        next_heading = re.search(r"^##\s+", text[start:end], flags=re.MULTILINE)
        if next_heading:
            end = start + next_heading.start()
        section = text[start:end].strip()
        if section:
            sections.append(section)
    return sections


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _as_posix(path: Path) -> str:
    return path.as_posix()
