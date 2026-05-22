from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from case_bank.__main__ import main as case_bank_main
from case_bank.index import build_indexes, discover_cases


def test_case_bank_index_build_succeeds_on_empty_cases_dir(tmp_path: Path) -> None:
    cases = tmp_path / "cases"
    indexes = tmp_path / "indexes"
    cases.mkdir()

    written = build_indexes(cases, indexes)

    assert len(written) == 5
    assert (indexes / "by-status.md").read_text(encoding="utf-8").startswith("# Cases By Status")


def test_case_bank_module_entrypoint_runs_from_repo_root() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)

    completed = subprocess.run(
        [sys.executable, "-B", "-m", "case_bank", "--help"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "{index,pack,validate}" in completed.stdout


def test_case_bank_pack_strips_hidden_files(tmp_path: Path) -> None:
    src = tmp_path / "cases"
    _write_valid_case_bank_case(src)

    out = tmp_path / "eval_package"

    assert case_bank_main(["pack", "--src", str(src), "--out", str(out)]) == 0
    packaged_case = out / "validation-and-policy" / "toy-case"
    assert (packaged_case / "client" / "probe.py").exists()
    assert not (packaged_case / "hidden").exists()
    assert not list(out.rglob("expected.json"))
    assert not list(out.rglob("oracle.md"))


def test_case_bank_validate_accepts_verified_package(tmp_path: Path) -> None:
    src = tmp_path / "cases"
    _write_valid_case_bank_case(src)

    assert case_bank_main(["validate", "--cases", str(src)]) == 0


def test_case_bank_validate_rejects_missing_expected(tmp_path: Path, capsys) -> None:
    src = tmp_path / "cases"
    case_dir = _write_valid_case_bank_case(src)
    (case_dir / "hidden" / "expected.json").unlink()

    assert case_bank_main(["validate", "--cases", str(src)]) == 1
    assert "hidden/expected.json" in capsys.readouterr().err


def test_committed_case_bank_has_verified_cases() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    cases = discover_cases(repo_root / "docs" / "case-bank" / "cases")
    ids = {case["case_id"] for case in cases}

    initial_ids = {
        "PY-SD-010",
        "JS-06",
        "JS-09",
        "GO-002",
        "RB-RACK-005",
        "PHP-07",
        "PHP-11",
        "PHP-12",
        "PHP-13",
        "JVM-JAVA-07",
        "DOTNET-08",
    }
    migrated_30_50_ids = {
        "DOTNET-05",
        "DOTNET-09",
        "GO-001",
        "GO-003",
        "GO-006",
        "GO-007",
        "JS-01",
        "JS-02",
        "JS-03",
        "JS-04",
        "JS-05",
        "JS-10",
        "JVM-JAVA-01",
        "JVM-JAVA-02",
        "JVM-JAVA-03",
        "JVM-JAVA-04",
        "RB-RSP-009",
        "RB-RACK-006",
        "PY-SD-008",
        "PY-SD-007",
        "PY-SD-005",
        "PY-SD-001",
        "PHP-08",
    }

    assert ids == initial_ids | migrated_30_50_ids
    for case in cases:
        case_dir = case["_path"]
        assert (case_dir / "client").is_dir()
        assert (case_dir / "hidden" / "expected.json").exists()
        expected = json.loads((case_dir / "hidden" / "expected.json").read_text(encoding="utf-8"))
        assert expected["case_id"] == case["case_id"]
        assert expected["assertions"]


def test_committed_case_bank_public_command_shapes_are_runnable() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    jvm_case = repo_root / "docs" / "case-bank" / "cases" / "parsing-and-ingestion" / "jvm-commons-csv-enum-header"
    dotnet_case = repo_root / "docs" / "case-bank" / "cases" / "validation-and-policy" / "dotnet-08-fluentvalidation-email"

    pom = (jvm_case / "client" / "pom.xml").read_text(encoding="utf-8")
    jvm_env = (jvm_case / "env.md").read_text(encoding="utf-8")
    dotnet_env = (dotnet_case / "env.md").read_text(encoding="utf-8")

    assert "<sourceDirectory>probe/src/main/java</sourceDirectory>" in pom
    assert "<mainClass>probe.Probe</mainClass>" in pom
    assert "compile exec:java" in jvm_env
    assert "dotnet run --project client/probe.csproj." in dotnet_env
    assert "--." not in dotnet_env


def _write_valid_case_bank_case(src: Path) -> Path:
    case_dir = src / "validation-and-policy" / "toy-case"
    hidden = case_dir / "hidden"
    client = case_dir / "client"
    hidden.mkdir(parents=True)
    client.mkdir()
    (case_dir / "case.md").write_text("# Toy\n", encoding="utf-8")
    (case_dir / "evidence.md").write_text("# Evidence\n", encoding="utf-8")
    (case_dir / "env.md").write_text("# Env\n", encoding="utf-8")
    (case_dir / "metadata.json").write_text(
        json.dumps(
            {
                "case_id": "TOY-001",
                "slug": "toy-case",
                "title": "Toy validation case",
                "status": "verified_keep",
                "primary_scenario": "validation-and-policy",
                "application_scenarios": ["validation-and-policy"],
                "ecosystems": ["python"],
                "languages": ["python"],
                "api_surfaces": ["library-api"],
                "drift_patterns": ["default-changed"],
                "failure_modes": ["silent-value-change"],
                "determinism": "local-deterministic",
                "external_dependencies": "package-cache",
                "old_version": "1.0.0",
                "new_version": "2.0.0",
                "source_urls": ["https://example.invalid/toy"],
                "provenance": {
                    "reproduction_result": "data/verification/toy",
                    "verified_at": "2026-05-21",
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (client / "probe.py").write_text("print('ok')\n", encoding="utf-8")
    (hidden / "oracle.md").write_text("# Oracle\n", encoding="utf-8")
    (hidden / "expected.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "case_id": "TOY-001",
                "assertions": [
                    {
                        "name": "value changes",
                        "field": "value",
                        "old": "old",
                        "new": "new",
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return case_dir
