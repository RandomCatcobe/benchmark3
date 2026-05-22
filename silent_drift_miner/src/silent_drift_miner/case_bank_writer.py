"""Bridge old workflow artifacts into case-bank source packages."""
from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from case_bank.schema import (
    DETERMINISM_VALUES,
    DRIFT_PATTERNS,
    FAILURE_MODES,
    PRIMARY_SCENARIOS,
    STATUS_VALUES,
    validate_metadata,
)

from .curation import load_curated_case
from .oracle import load_oracle_spec
from .reproduction import (
    DEFAULT_IGNORED_JSON_FIELDS,
    DropReason,
    ReproductionResult,
    load_reproduction_result,
    load_reproduction_spec,
)
from .schema import utc_now_iso


EXCLUDED_CLIENT_NAMES = {
    ".git",
    ".gradle",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "bin",
    "build",
    "dist",
    "node_modules",
    "obj",
    "target",
    "vendor",
    "venv",
}
EXCLUDED_CLIENT_PATTERNS = ("*.pyc", "*.pyo", "*.class", "*.jar", "*.log", "*.tmp")


@dataclass
class CaseBankPackageRequest:
    reproduction_result: Path
    client: Path
    out_root: Path
    primary_scenario: str
    case_id: str
    candidate: Path | None = None
    slug: str | None = None
    title: str | None = None
    status: str | None = None
    source_urls: list[str] = field(default_factory=list)
    source_excerpt: str | None = None
    retrieved_at: str | None = None
    ecosystem: str | None = None
    languages: list[str] = field(default_factory=list)
    api_surfaces: list[str] = field(default_factory=list)
    application_scenarios: list[str] = field(default_factory=list)
    drift_patterns: list[str] = field(default_factory=list)
    failure_modes: list[str] = field(default_factory=list)
    determinism: str = "local-deterministic"
    external_dependencies: str = "package-cache"
    review_notes: str | None = None
    oracle_spec: Path | None = None
    overwrite: bool = False


def create_case_bank_package(request: CaseBankPackageRequest) -> Path:
    """Create one case-bank source package from old workflow artifacts."""
    candidate = _load_candidate(request.candidate)
    result = load_reproduction_result(request.reproduction_result)

    status = _derive_status(result, request.status)
    _validate_choice("primary_scenario", request.primary_scenario, PRIMARY_SCENARIOS)
    slug = _validated_slug(request.slug or _slug(request.case_id))
    package_dir = _package_dir(request.out_root, request.primary_scenario, slug)
    metadata = _build_metadata(request, candidate, result, status, slug)
    validate_metadata(metadata, package_dir / "metadata.json")
    _validate_client_source(request.client)
    hidden_oracle = ""
    hidden_expected: dict[str, Any] | None = None
    if status == "verified_keep":
        hidden_expected = _expected_payload(metadata, result)
        hidden_oracle = _oracle_markdown(metadata, hidden_expected["assertions"][0])

    if package_dir.exists():
        if not request.overwrite:
            raise ValueError(f"case-bank package already exists: {package_dir}")
        shutil.rmtree(package_dir)

    package_dir.mkdir(parents=True, exist_ok=True)
    _copy_client(request.client, package_dir / "client")
    (package_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (package_dir / "case.md").write_text(
        _case_markdown(metadata, candidate, result),
        encoding="utf-8",
    )
    (package_dir / "evidence.md").write_text(
        _evidence_markdown(metadata, request, candidate, result),
        encoding="utf-8",
    )
    (package_dir / "env.md").write_text(
        _env_markdown(request, result),
        encoding="utf-8",
    )
    if status == "verified_keep":
        if hidden_expected is None:
            raise AssertionError("verified case expected payload was not prepared")
        hidden_dir = package_dir / "hidden"
        hidden_dir.mkdir()
        (hidden_dir / "oracle.md").write_text(
            hidden_oracle,
            encoding="utf-8",
        )
        (hidden_dir / "expected.json").write_text(
            json.dumps(hidden_expected, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    return package_dir


def create_case_bank_package_from_curated(
    case_path: Path,
    oracle_path: Path,
    client: Path,
    out_root: Path,
    primary_scenario: str,
    *,
    slug: str | None = None,
    title: str | None = None,
    application_scenarios: list[str] | None = None,
    drift_patterns: list[str] | None = None,
    failure_modes: list[str] | None = None,
    determinism: str = "local-deterministic",
    external_dependencies: str = "package-cache",
    overwrite: bool = False,
) -> Path:
    """Create a case-bank package from a curated case plus oracle artifact."""
    if not oracle_path.is_file():
        raise ValueError(f"oracle spec not found: {oracle_path}")
    curated = load_curated_case(case_path)
    oracle = load_oracle_spec(oracle_path)
    if oracle.case_id != curated.case_id:
        raise ValueError(f"oracle case_id {oracle.case_id!r} does not match curated case_id {curated.case_id!r}")
    if oracle.candidate_id != curated.candidate_id:
        raise ValueError(
            f"oracle candidate_id {oracle.candidate_id!r} does not match curated candidate_id {curated.candidate_id!r}"
        )
    result_path = _resolve_link(case_path, curated.reproduction_result)
    request = CaseBankPackageRequest(
        reproduction_result=result_path,
        client=client,
        out_root=out_root,
        primary_scenario=primary_scenario,
        case_id=curated.case_id,
        slug=slug,
        title=title,
        source_urls=[curated.source_url] if curated.source_url else [],
        source_excerpt=curated.source_excerpt,
        retrieved_at=curated.retrieved_at,
        ecosystem=curated.ecosystem,
        api_surfaces=curated.api_surface,
        application_scenarios=list(application_scenarios or []),
        drift_patterns=list(drift_patterns or []),
        failure_modes=list(failure_modes or []),
        determinism=determinism,
        external_dependencies=external_dependencies,
        review_notes=curated.review_notes,
        oracle_spec=oracle_path,
        overwrite=overwrite,
    )
    return create_case_bank_package(request)


def _build_metadata(
    request: CaseBankPackageRequest,
    candidate: dict[str, Any],
    result: ReproductionResult,
    status: str,
    slug: str,
) -> dict[str, Any]:
    _validate_choice("status", status, STATUS_VALUES)
    _validate_choice("primary_scenario", request.primary_scenario, PRIMARY_SCENARIOS)
    _validate_choice("determinism", request.determinism, DETERMINISM_VALUES)
    _validate_choice("external_dependencies", request.external_dependencies, DETERMINISM_VALUES)

    title = request.title or candidate.get("title") or _title_from_slug(slug)
    ecosystem = request.ecosystem or candidate.get("ecosystem") or "python"
    language = _ecosystem_to_language(ecosystem)
    source_urls = _source_urls(request, candidate)
    application_scenarios = _ordered_unique([request.primary_scenario, *request.application_scenarios])
    drift_patterns = _nonempty_allowed(
        "drift_patterns",
        request.drift_patterns or _candidate_list(candidate, "drift_patterns"),
        DRIFT_PATTERNS,
        "default-changed",
    )
    failure_modes = _nonempty_allowed(
        "failure_modes",
        request.failure_modes or _candidate_list(candidate, "failure_modes"),
        FAILURE_MODES,
        "silent-value-change",
    )
    api_surfaces = _ordered_unique(
        [*request.api_surfaces, *_candidate_list(candidate, "api_surface"), *_candidate_list(candidate, "api_surfaces")]
    ) or ["library-api"]
    provenance = {
        "reproduction_result": _friendly_path(request.reproduction_result),
        "verified_at": request.retrieved_at or candidate.get("retrieved_at") or utc_now_iso(),
        "candidate_id": result.candidate_id,
        "original_status": _original_status(result),
        "first_blocker": _first_blocker(result),
    }
    if request.candidate:
        provenance["candidate"] = _friendly_path(request.candidate)
        old_case_path = _old_case_path(request.candidate)
        if old_case_path:
            provenance["old_case_path"] = old_case_path
            provenance["old_case_id"] = str(candidate.get("case_id") or request.candidate.parent.name)
    if request.oracle_spec:
        provenance["oracle_spec"] = _friendly_path(request.oracle_spec)

    metadata = {
        "case_id": request.case_id,
        "slug": slug,
        "title": title,
        "status": status,
        "primary_scenario": request.primary_scenario,
        "application_scenarios": application_scenarios,
        "ecosystems": [ecosystem],
        "languages": _ordered_unique([*request.languages, language]),
        "api_surfaces": api_surfaces,
        "drift_patterns": drift_patterns,
        "failure_modes": failure_modes,
        "determinism": request.determinism,
        "external_dependencies": request.external_dependencies,
        "old_version": _version(candidate, result, "old"),
        "new_version": _version(candidate, result, "new"),
        "source_urls": source_urls,
        "provenance": provenance,
    }
    return metadata


def _case_markdown(metadata: dict[str, Any], candidate: dict[str, Any], result: ReproductionResult) -> str:
    summary = candidate.get("summary_paraphrased") or candidate.get("summary") or "Generated from old workflow artifacts."
    hypothesis = candidate.get("reproduce_hypothesis") or "Run the public client against the old and new environments."
    if result.keep:
        observed = "The old and new runs both completed and produced a meaningful behavior difference."
        silent = "The public call shape remains runnable on both sides."
    elif result.drop_reason == DropReason.NO_BEHAVIOR_DIFF:
        observed = "The replay completed, but no meaningful behavior difference remained."
        silent = "No verified silent drift is recorded for this replay."
    else:
        observed = "The replay did not complete as a verified silent-drift case."
        silent = "The first blocker is preserved for future retry."

    return "\n".join(
        [
            f"# {metadata['case_id']}: {metadata['title']}",
            "",
            "## API Or Behavior Under Test",
            "",
            str(hypothesis),
            "",
            "## Version Boundary",
            "",
            f"{metadata['old_version']} -> {metadata['new_version']}",
            "",
            "## Public Summary",
            "",
            str(summary),
            "",
            "## Replay Outcome",
            "",
            observed,
            "",
            "## Why This Is Or Is Not Silent Drift",
            "",
            silent,
            "",
        ]
    )


def _evidence_markdown(
    metadata: dict[str, Any],
    request: CaseBankPackageRequest,
    candidate: dict[str, Any],
    result: ReproductionResult,
) -> str:
    excerpt = request.source_excerpt or candidate.get("excerpt") or candidate.get("source_excerpt")
    if not excerpt:
        excerpt = "No source excerpt was supplied; provenance is recorded through the candidate and replay artifacts."
    notes = request.review_notes or candidate.get("review_notes") or "No review notes supplied."
    source_urls = metadata["source_urls"] or ["No source URL supplied."]
    blocker = _first_blocker(result) or "none"
    return "\n".join(
        [
            f"# Evidence For {metadata['case_id']}",
            "",
            "## Sources",
            "",
            *[f"- {url}" for url in source_urls],
            "",
            "## Source Excerpt Or Provenance Note",
            "",
            str(excerpt),
            "",
            "## Version Boundary",
            "",
            f"- Old version: {metadata['old_version']}",
            f"- New version: {metadata['new_version']}",
            "",
            "## Replay Artifact",
            "",
            f"- Result: {_friendly_path(request.reproduction_result)}",
            f"- Status: {metadata['status']}",
            f"- Diff summary: {result.diff.summary}",
            f"- First blocker: {blocker}",
            "",
            "## Review Notes",
            "",
            str(notes),
            "",
        ]
    )


def _env_markdown(request: CaseBankPackageRequest, result: ReproductionResult) -> str:
    lines = [
        f"# Environment For {request.case_id}",
        "",
        "## Inputs",
        "",
        f"- Reproduction result: {_friendly_path(request.reproduction_result)}",
        f"- Client source: {_friendly_path(request.client)}",
        f"- Old side: {result.old_run.environment.library} {result.old_run.environment.version}",
        f"- New side: {result.new_run.environment.library} {result.new_run.environment.version}",
        "",
        "## Command Shape",
        "",
    ]
    spec_path = Path(result.spec_path)
    if spec_path.exists():
        lines.append(f"Rerun with: `silent-drift-miner reproduce run --spec {_friendly_path(spec_path)} --out <attempt-root>`")
        try:
            spec = load_reproduction_spec(spec_path)
            lines.extend(
                [
                    "",
                    f"- Client file in spec: `{spec.client_file}`",
                    f"- Old install command: `{' '.join(spec.old_environment.install_command)}`",
                    f"- New install command: `{' '.join(spec.new_environment.install_command)}`",
                ]
            )
        except Exception:
            lines.append("The spec path exists, but could not be parsed by the current loader.")
    else:
        lines.append("The original spec path was not available; use the recorded result paths and copied client.")
    lines.extend(
        [
            "",
            "## Local Run Logs",
            "",
            f"- Old stdout: {_friendly_path(Path(result.old_run.stdout_path))}",
            f"- Old stderr: {_friendly_path(Path(result.old_run.stderr_path))}",
            f"- New stdout: {_friendly_path(Path(result.new_run.stdout_path))}",
            f"- New stderr: {_friendly_path(Path(result.new_run.stderr_path))}",
            "",
        ]
    )
    return "\n".join(lines)


def _oracle_markdown(metadata: dict[str, Any], assertion: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"# Oracle For {metadata['case_id']}",
            "",
            "Compare the old-version and new-version probe outputs after normalizing runtime log noise.",
            "",
            "Required assertion:",
            "",
            f"- {assertion['name']}: `{assertion['field']}` old={assertion['old']!r} new={assertion['new']!r}",
            "",
        ]
    )


def _expected_payload(metadata: dict[str, Any], result: ReproductionResult) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "case_id": metadata["case_id"],
        "assertions": [_first_assertion(result)],
    }


def _first_assertion(result: ReproductionResult) -> dict[str, Any]:
    old_stdout = _read_text(Path(result.old_run.stdout_path)).strip()
    new_stdout = _read_text(Path(result.new_run.stdout_path)).strip()
    old_value, old_structured = _parse_jsonish(old_stdout)
    new_value, new_structured = _parse_jsonish(new_stdout)
    diff = _first_difference(old_value, new_value, ignored_fields=_ignored_json_fields(result))
    if diff is not None:
        field, old, new = diff
        return {"name": f"{field} changes", "field": field, "old": old, "new": new}
    if old_structured or new_structured:
        raise ValueError("verified case has no non-ignored behavior assertion")
    if old_stdout == new_stdout:
        raise ValueError("verified case has no stdout behavior difference")
    return {
        "name": "stdout changes",
        "field": "stdout",
        "old": old_stdout,
        "new": new_stdout,
    }


def _derive_status(result: ReproductionResult, override: str | None) -> str:
    if override:
        _validate_choice("status", override, STATUS_VALUES)
        return override
    if result.keep and result.diff.changed:
        return "verified_keep"
    if result.drop_reason == DropReason.NO_BEHAVIOR_DIFF:
        return "rejected_no_diff"
    if result.drop_reason in {DropReason.INSTALL_FAILED, DropReason.IMPORT_FAILED}:
        return "blocked_dependency"
    if result.drop_reason in {DropReason.CLIENT_RUNTIME_ERROR, DropReason.HARD_BREAK, DropReason.TIMEOUT}:
        return "blocked_runtime"
    return "needs_source"


def _original_status(result: ReproductionResult) -> str:
    if result.keep:
        return "verified_keep"
    if result.drop_reason:
        return result.drop_reason.value
    return "needs_source"


def _first_blocker(result: ReproductionResult) -> str:
    if result.keep:
        return ""
    if result.drop_reason:
        reason = result.drop_reason.value
    else:
        reason = "unknown"
    details = []
    for label, run in (("old", result.old_run), ("new", result.new_run)):
        if run.build_exit_code not in (None, 0):
            details.append(f"{label} build exit {run.build_exit_code}")
        if run.exit_code not in (None, 0):
            details.append(f"{label} run exit {run.exit_code}")
        stderr = _read_text(Path(run.stderr_path)).strip()
        if stderr:
            details.append(f"{label} stderr: {_one_line(stderr)}")
    return reason if not details else reason + " - " + "; ".join(details)


def _source_urls(request: CaseBankPackageRequest, candidate: dict[str, Any]) -> list[str]:
    urls: list[str] = []
    urls.extend(request.source_urls)
    raw = candidate.get("source_url")
    if isinstance(raw, str) and raw:
        urls.append(raw)
    raw_urls = candidate.get("source_urls")
    if isinstance(raw_urls, list):
        urls.extend(str(url) for url in raw_urls if url)
    evidence = candidate.get("evidence")
    if isinstance(evidence, list):
        for item in evidence:
            if isinstance(item, dict) and item.get("url"):
                urls.append(str(item["url"]))
    return _ordered_unique(urls) or ["https://example.invalid/source-unavailable"]


def _version(candidate: dict[str, Any], result: ReproductionResult, side: str) -> str:
    key = f"version_{side}"
    if candidate.get(key):
        return str(candidate[key])
    run = result.old_run if side == "old" else result.new_run
    return run.environment.version or "unknown"


def _candidate_list(candidate: dict[str, Any], key: str) -> list[str]:
    value = candidate.get(key)
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, str) and value:
        return [value]
    return []


def _copy_client(source: Path, destination: Path) -> None:
    _validate_client_source(source)
    if source.is_dir():
        shutil.copytree(source, destination, ignore=_ignore_client_artifacts)
    else:
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination / source.name)


def _validate_client_source(source: Path) -> None:
    if not source.exists():
        raise ValueError(f"client source not found: {source}")
    if not source.is_dir() and _is_excluded_client_path(source):
        raise ValueError(f"client source is excluded from public packages: {source}")


def _ignore_client_artifacts(directory: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        path = Path(directory) / name
        if name in EXCLUDED_CLIENT_NAMES or _is_excluded_client_path(path):
            ignored.add(name)
    return ignored


def _is_excluded_client_path(path: Path) -> bool:
    name = path.name
    suffix = path.suffix.lower()
    if name in EXCLUDED_CLIENT_NAMES:
        return True
    if suffix in {".pyc", ".pyo", ".class", ".jar"}:
        return True
    return any(path.match(pattern) for pattern in EXCLUDED_CLIENT_PATTERNS)


def _load_candidate(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    if not path.is_file():
        raise ValueError(f"candidate not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("candidate JSON must be an object")
    return data


def _parse_jsonish(text: str) -> tuple[Any, bool]:
    try:
        return json.loads(text), True
    except json.JSONDecodeError:
        pass
    lines = [line for line in text.splitlines() if line.strip()]
    parsed_lines = []
    for line in lines:
        try:
            parsed_lines.append(json.loads(line))
        except json.JSONDecodeError:
            return text, False
    return (parsed_lines, True) if parsed_lines else (text, False)


def _first_difference(
    old: Any,
    new: Any,
    prefix: str = "",
    ignored_fields: list[str] | None = None,
) -> tuple[str, Any, Any] | None:
    ignored = set(DEFAULT_IGNORED_JSON_FIELDS if ignored_fields is None else ignored_fields)
    if isinstance(old, dict) and isinstance(new, dict):
        for key in sorted(set(old) | set(new)):
            if key in ignored:
                continue
            field = f"{prefix}.{key}" if prefix else str(key)
            if key not in old or key not in new:
                return field, old.get(key), new.get(key)
            diff = _first_difference(old[key], new[key], field, ignored_fields)
            if diff is not None:
                return diff
        return None
    if isinstance(old, list) and isinstance(new, list):
        for index in range(max(len(old), len(new))):
            field = f"{prefix}[{index}]" if prefix else f"[{index}]"
            if index >= len(old) or index >= len(new):
                return field, old[index] if index < len(old) else None, new[index] if index < len(new) else None
            diff = _first_difference(old[index], new[index], field, ignored_fields)
            if diff is not None:
                return diff
        return None
    if old != new:
        return prefix or "value", old, new
    return None


def _nonempty_allowed(field_name: str, values: list[str], allowed: set[str], default: str) -> list[str]:
    selected = _ordered_unique(values) or [default]
    for value in selected:
        _validate_choice(field_name, value, allowed)
    return selected


def _validate_choice(field_name: str, value: str, allowed: set[str]) -> None:
    if value not in allowed:
        raise ValueError(f"{field_name} must be one of {sorted(allowed)}, got {value!r}")


def _ordered_unique(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _ecosystem_to_language(ecosystem: str) -> str:
    return {
        "dotnet": "csharp",
        "go": "go",
        "jvm": "java",
        "js": "javascript",
        "php": "php",
        "python": "python",
        "ruby": "ruby",
    }.get(ecosystem, ecosystem)


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.lower()).strip("-")
    return slug or "case"


def _validated_slug(value: str) -> str:
    if not value or value in {".", ".."}:
        raise ValueError(f"slug must be a safe single path segment, got {value!r}")
    if "/" in value or "\\" in value:
        raise ValueError(f"slug must be a safe single path segment, got {value!r}")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", value):
        raise ValueError(f"slug must be a safe single path segment, got {value!r}")
    return value


def _package_dir(out_root: Path, primary_scenario: str, slug: str) -> Path:
    scenario_root = out_root / primary_scenario
    package_dir = scenario_root / slug
    try:
        package_dir.resolve().relative_to(scenario_root.resolve())
    except ValueError as exc:
        raise ValueError(f"case-bank package path escapes scenario root: {package_dir}") from exc
    return package_dir


def _ignored_json_fields(result: ReproductionResult) -> list[str]:
    details_ignored = result.diff.details.get("ignored_json_fields")
    if isinstance(details_ignored, list) and all(isinstance(item, str) for item in details_ignored):
        return list(details_ignored)
    try:
        spec = load_reproduction_spec(Path(result.spec_path))
    except Exception:
        return list(DEFAULT_IGNORED_JSON_FIELDS)
    return list(spec.comparison_policy.ignore_json_fields)


def _title_from_slug(slug: str) -> str:
    return " ".join(part for part in re.split(r"[-_]+", slug) if part).title() or slug


def _friendly_path(path: Path) -> str:
    try:
        return Path(path).resolve().relative_to(Path.cwd().resolve()).as_posix()
    except Exception:
        return str(path)


def _old_case_path(candidate_path: Path) -> str:
    try:
        path = candidate_path.resolve()
        relative = path.relative_to(Path.cwd().resolve())
    except Exception:
        return ""
    parts = relative.parts
    if len(parts) >= 3 and parts[0] == "cases" and parts[-1] == "candidate.json":
        return Path(*parts[:-1]).as_posix()
    return ""


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _one_line(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()[:240]


def _resolve_link(base_file: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return base_file.parent / path
