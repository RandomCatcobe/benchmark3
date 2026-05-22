"""Validation gates for case-bank source packages."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .schema import load_metadata


REQUIRED_CASE_FILES = ("case.md", "evidence.md", "env.md", "metadata.json")


@dataclass
class CaseBankValidationResult:
    checked_cases: int = 0
    findings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.findings


def validate_cases(cases_root: Path) -> CaseBankValidationResult:
    result = CaseBankValidationResult()
    if not cases_root.exists():
        result.findings.append(f"case root does not exist: {cases_root}")
        return result
    if not cases_root.is_dir():
        result.findings.append(f"case root must be a directory: {cases_root}")
        return result

    metadata_paths = sorted(cases_root.rglob("metadata.json"))
    case_dirs = {path.parent for path in metadata_paths}
    case_dirs.update(_case_like_dirs(cases_root))

    for case_dir in sorted(case_dirs):
        _validate_case_dir(case_dir, result)
    return result


def validate_expected_payload(data: dict[str, Any], path: Path | None = None, case_id: str | None = None) -> None:
    label = str(path) if path else "expected.json"
    if not isinstance(data.get("schema_version"), int):
        raise ValueError(f"{label}: schema_version must be an integer")
    if not isinstance(data.get("case_id"), str) or not data["case_id"]:
        raise ValueError(f"{label}: case_id must be a non-empty string")
    if case_id is not None and data["case_id"] != case_id:
        raise ValueError(f"{label}: case_id {data['case_id']!r} does not match metadata {case_id!r}")

    assertions = data.get("assertions")
    if not isinstance(assertions, list) or not assertions:
        raise ValueError(f"{label}: assertions must be a non-empty list")
    for index, assertion in enumerate(assertions, start=1):
        _validate_assertion(label, index, assertion)


def expected_json_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://silentdrift.local/case-bank/expected.schema.json",
        "title": "SilentDrift Case Bank Expected Assertions",
        "type": "object",
        "additionalProperties": True,
        "required": ["schema_version", "case_id", "assertions"],
        "properties": {
            "schema_version": {"type": "integer"},
            "case_id": {"type": "string", "minLength": 1},
            "assertions": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "additionalProperties": True,
                    "required": ["name", "field", "old", "new"],
                    "properties": {
                        "name": {"type": "string", "minLength": 1},
                        "field": {"type": "string", "minLength": 1},
                    },
                },
            },
        },
    }


def write_expected_schema(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(expected_json_schema(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _validate_case_dir(case_dir: Path, result: CaseBankValidationResult) -> None:
    result.checked_cases += 1
    for filename in REQUIRED_CASE_FILES:
        if not (case_dir / filename).is_file():
            result.findings.append(f"{case_dir}: missing {filename}")
    if not (case_dir / "client").is_dir():
        result.findings.append(f"{case_dir}: missing client/")

    metadata_path = case_dir / "metadata.json"
    try:
        metadata = load_metadata(metadata_path)
    except Exception as exc:
        result.findings.append(f"{metadata_path}: {exc}")
        return

    if metadata["slug"] != case_dir.name:
        result.findings.append(f"{metadata_path}: slug {metadata['slug']!r} does not match folder {case_dir.name!r}")
    if metadata["status"] == "verified_keep":
        _validate_verified_hidden_material(case_dir, metadata["case_id"], result)


def _validate_verified_hidden_material(
    case_dir: Path,
    case_id: str,
    result: CaseBankValidationResult,
) -> None:
    hidden_dir = case_dir / "hidden"
    oracle_path = hidden_dir / "oracle.md"
    expected_path = hidden_dir / "expected.json"
    if not oracle_path.is_file():
        result.findings.append(f"{case_dir}: verified case missing hidden/oracle.md")
    if not expected_path.is_file():
        result.findings.append(f"{case_dir}: verified case missing hidden/expected.json")
        return
    try:
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        validate_expected_payload(expected, expected_path, case_id)
    except Exception as exc:
        result.findings.append(str(exc))


def _validate_assertion(label: str, index: int, assertion: Any) -> None:
    if not isinstance(assertion, dict):
        raise ValueError(f"{label}: assertion {index} must be an object")
    for field in ("name", "field"):
        if not isinstance(assertion.get(field), str) or not assertion[field]:
            raise ValueError(f"{label}: assertion {index} field {field!r} must be a non-empty string")
    for field in ("old", "new"):
        if field not in assertion:
            raise ValueError(f"{label}: assertion {index} missing field {field!r}")
    if assertion["old"] == assertion["new"]:
        raise ValueError(f"{label}: assertion {index} old and new values must differ")


def _case_like_dirs(cases_root: Path) -> set[Path]:
    markers = {"case.md", "evidence.md", "env.md"}
    dirs: set[Path] = set()
    for path in cases_root.rglob("*"):
        if path.is_file() and path.name in markers:
            dirs.add(path.parent)
        elif path.is_dir() and path.name in {"client", "hidden"}:
            dirs.add(path.parent)
    return dirs
