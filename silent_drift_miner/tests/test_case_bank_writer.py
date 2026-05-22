from __future__ import annotations

import json
from pathlib import Path

from case_bank.__main__ import main as case_bank_main
from case_bank.validation import validate_cases
from silent_drift_miner.cli import main


def test_case_bank_create_verified_package_validates_and_packs(tmp_path: Path) -> None:
    result = _write_reproduction_result(
        tmp_path,
        "verified",
        old_stdout='{"value": "old", "library_version": "1.0.0"}',
        new_stdout='{"value": "new", "library_version": "2.0.0"}',
        keep=True,
    )
    candidate = _write_candidate(tmp_path)
    client = _write_client(tmp_path)
    out = tmp_path / "case-bank-cases"

    assert _create_case(out, result, candidate, client) == 0

    case_dir = out / "validation-and-policy" / "toy-case"
    metadata = json.loads((case_dir / "metadata.json").read_text(encoding="utf-8"))
    expected = json.loads((case_dir / "hidden" / "expected.json").read_text(encoding="utf-8"))

    assert metadata["status"] == "verified_keep"
    assert expected["assertions"][0]["field"] == "value"
    assert expected["assertions"][0]["old"] == "old"
    assert expected["assertions"][0]["new"] == "new"
    assert validate_cases(out).ok

    packaged = tmp_path / "eval-package"
    assert case_bank_main(["pack", "--src", str(out), "--out", str(packaged)]) == 0
    assert (packaged / "validation-and-policy" / "toy-case" / "client" / "client.py").exists()
    assert not list(packaged.rglob("hidden"))
    assert not list(packaged.rglob("expected.json"))
    assert not list(packaged.rglob("oracle.md"))


def test_case_bank_create_rejected_no_diff_has_no_hidden_oracle(tmp_path: Path) -> None:
    result = _write_reproduction_result(
        tmp_path,
        "no-diff",
        old_stdout='{"value": "same"}',
        new_stdout='{"value": "same"}',
        keep=False,
        drop_reason="no_behavior_diff",
    )
    out = tmp_path / "case-bank-cases"

    assert _create_case(out, result, _write_candidate(tmp_path), _write_client(tmp_path)) == 0

    case_dir = out / "validation-and-policy" / "toy-case"
    metadata = json.loads((case_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["status"] == "rejected_no_diff"
    assert metadata["provenance"]["original_status"] == "no_behavior_diff"
    assert not (case_dir / "hidden").exists()
    assert validate_cases(out).ok


def test_case_bank_create_blocked_dependency_records_first_blocker(tmp_path: Path) -> None:
    result = _write_reproduction_result(
        tmp_path,
        "blocked",
        old_stdout="",
        new_stdout="",
        old_stderr="ModuleNotFoundError: No module named 'toy_drift'",
        keep=False,
        drop_reason="import_failed",
        old_exit_code=1,
    )
    out = tmp_path / "case-bank-cases"

    assert _create_case(out, result, _write_candidate(tmp_path), _write_client(tmp_path)) == 0

    case_dir = out / "validation-and-policy" / "toy-case"
    metadata = json.loads((case_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["status"] == "blocked_dependency"
    assert "import_failed" in metadata["provenance"]["first_blocker"]
    assert "ModuleNotFoundError" in metadata["provenance"]["first_blocker"]
    assert not (case_dir / "hidden").exists()
    assert validate_cases(out).ok


def test_case_bank_create_refuses_to_overwrite_by_default(tmp_path: Path) -> None:
    result = _write_reproduction_result(
        tmp_path,
        "verified",
        old_stdout='{"value": "old"}',
        new_stdout='{"value": "new"}',
        keep=True,
    )
    candidate = _write_candidate(tmp_path)
    client = _write_client(tmp_path)
    out = tmp_path / "case-bank-cases"

    assert _create_case(out, result, candidate, client) == 0
    assert _create_case(out, result, candidate, client) == 1


def test_case_bank_create_rejects_path_traversal_slug(tmp_path: Path) -> None:
    result = _write_reproduction_result(
        tmp_path,
        "verified",
        old_stdout='{"value": "old"}',
        new_stdout='{"value": "new"}',
        keep=True,
    )
    out = tmp_path / "case-bank-cases"

    code = main(
        [
            "case-bank",
            "create",
            "--reproduction-result",
            str(result),
            "--candidate",
            str(_write_candidate(tmp_path)),
            "--client",
            str(_write_client(tmp_path)),
            "--case-id",
            "TOY-001",
            "--slug",
            "../escaped",
            "--primary-scenario",
            "validation-and-policy",
            "--out-root",
            str(out),
        ]
    )

    assert code == 1
    assert not (tmp_path / "escaped").exists()


def test_case_bank_create_rejects_version_only_verified_assertion(tmp_path: Path) -> None:
    result = _write_reproduction_result(
        tmp_path,
        "version-only",
        old_stdout='{"library_version": "1.0.0"}',
        new_stdout='{"library_version": "2.0.0"}',
        keep=True,
    )
    out = tmp_path / "case-bank-cases"

    assert _create_case(out, result, _write_candidate(tmp_path), _write_client(tmp_path)) == 1
    assert not (out / "validation-and-policy" / "toy-case").exists()


def test_case_bank_create_strips_gradle_cache_from_client_dir(tmp_path: Path) -> None:
    result = _write_reproduction_result(
        tmp_path,
        "verified",
        old_stdout='{"value": "old"}',
        new_stdout='{"value": "new"}',
        keep=True,
    )
    client = tmp_path / "client-dir"
    (client / ".gradle").mkdir(parents=True)
    (client / ".gradle" / "cache.bin").write_text("cache", encoding="utf-8")
    (client / "probe.py").write_text("print('ok')\n", encoding="utf-8")
    out = tmp_path / "case-bank-cases"

    assert _create_case(out, result, _write_candidate(tmp_path), client) == 0

    copied = out / "validation-and-policy" / "toy-case" / "client"
    assert (copied / "probe.py").exists()
    assert not (copied / ".gradle").exists()


def test_case_bank_from_curated_creates_verified_package(tmp_path: Path) -> None:
    result = _write_reproduction_result(
        tmp_path,
        "verified",
        old_stdout='{"value": "old"}',
        new_stdout='{"value": "new"}',
        keep=True,
    )
    case = tmp_path / "curated" / "case.yaml"
    oracle = tmp_path / "oracle" / "oracle_spec.yaml"
    _write_oracle_spec(oracle)
    case.parent.mkdir()
    case.write_text(
        "\n".join(
            [
                'case_id: "TOY-001"',
                'decision: "accept"',
                'candidate_id: "toy-candidate"',
                f'reproduction_result: "{result.as_posix()}"',
                "keep: true",
                "drop_reason: null",
                'source_url: "https://example.invalid/toy"',
                'source_excerpt: "Toy source excerpt."',
                'retrieved_at: "2026-05-22"',
                'ecosystem: "python"',
                'version_old: "1.0.0"',
                'version_new: "2.0.0"',
                'api_surface: ["toy.value"]',
                'review_notes: "Curated test case."',
                'schema_version: "1"',
                'created_at: "2026-05-22T00:00:00"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    out = tmp_path / "case-bank-cases"

    assert main(
        [
            "case-bank",
            "from-curated",
            "--case",
            str(case),
            "--oracle",
            str(oracle),
            "--client",
            str(_write_client(tmp_path)),
            "--primary-scenario",
            "validation-and-policy",
            "--out-root",
            str(out),
        ]
    ) == 0
    assert validate_cases(out).ok
    assert (out / "validation-and-policy" / "toy-001" / "hidden" / "expected.json").exists()


def test_case_bank_from_curated_rejects_oracle_case_id_mismatch(tmp_path: Path) -> None:
    result = _write_reproduction_result(
        tmp_path,
        "verified",
        old_stdout='{"value": "old"}',
        new_stdout='{"value": "new"}',
        keep=True,
    )
    case = tmp_path / "curated" / "case.yaml"
    oracle = tmp_path / "oracle" / "oracle_spec.yaml"
    _write_oracle_spec(oracle, case_id="OTHER-001")
    case.parent.mkdir()
    case.write_text(
        "\n".join(
            [
                'case_id: "TOY-001"',
                'decision: "accept"',
                'candidate_id: "toy-candidate"',
                f'reproduction_result: "{result.as_posix()}"',
                "keep: true",
                "drop_reason: null",
                'source_url: "https://example.invalid/toy"',
                'source_excerpt: "Toy source excerpt."',
                'retrieved_at: "2026-05-22"',
                'ecosystem: "python"',
                'version_old: "1.0.0"',
                'version_new: "2.0.0"',
                'api_surface: ["toy.value"]',
                'review_notes: "Curated test case."',
                'schema_version: "1"',
                'created_at: "2026-05-22T00:00:00"',
                "",
            ]
        ),
        encoding="utf-8",
    )

    assert main(
        [
            "case-bank",
            "from-curated",
            "--case",
            str(case),
            "--oracle",
            str(oracle),
            "--client",
            str(_write_client(tmp_path)),
            "--primary-scenario",
            "validation-and-policy",
            "--out-root",
            str(tmp_path / "case-bank-cases"),
        ]
    ) == 1


def _create_case(out: Path, result: Path, candidate: Path, client: Path) -> int:
    return main(
        [
            "case-bank",
            "create",
            "--reproduction-result",
            str(result),
            "--candidate",
            str(candidate),
            "--client",
            str(client),
            "--case-id",
            "TOY-001",
            "--slug",
            "toy-case",
            "--primary-scenario",
            "validation-and-policy",
            "--out-root",
            str(out),
        ]
    )


def _write_candidate(tmp_path: Path) -> Path:
    path = tmp_path / "candidate.json"
    path.write_text(
        json.dumps(
            {
                "candidate_id": "toy-candidate",
                "title": "Toy case-bank bridge case",
                "summary_paraphrased": "A toy value changes between versions.",
                "reproduce_hypothesis": "Read toy_drift.value from the public client.",
                "library": "toy-drift",
                "ecosystem": "python",
                "version_old": "1.0.0",
                "version_new": "2.0.0",
                "api_surface": ["toy_drift.value"],
                "source_url": "https://example.invalid/toy-release",
                "excerpt": "The toy default value changed.",
                "retrieved_at": "2026-05-22",
                "review_notes": "Synthetic writer test fixture.",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def _write_client(tmp_path: Path) -> Path:
    path = tmp_path / "client.py"
    path.write_text("import toy_drift\nprint(toy_drift.value())\n", encoding="utf-8")
    return path


def _write_oracle_spec(path: Path, *, case_id: str = "TOY-001", candidate_id: str = "toy-candidate") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                f'case_id: "{case_id}"',
                f'candidate_id: "{candidate_id}"',
                'case_path: "case.yaml"',
                'template: "pytest"',
                'hidden_test_path: "hidden/test_behavior.py"',
                'expected_path: "hidden/expected.json"',
                'public_readme_path: "public/README.md"',
                'starter_client_path: "public/starter_client.py"',
                'schema_version: "1"',
                'created_at: "2026-05-22T00:00:00"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    return path


def _write_reproduction_result(
    tmp_path: Path,
    name: str,
    *,
    old_stdout: str,
    new_stdout: str,
    keep: bool,
    drop_reason: str | None = None,
    old_stderr: str = "",
    new_stderr: str = "",
    old_exit_code: int = 0,
    new_exit_code: int = 0,
) -> Path:
    attempt = tmp_path / "repro" / name / "attempt_001"
    old = attempt / "old"
    new = attempt / "new"
    old.mkdir(parents=True)
    new.mkdir()
    spec = attempt / "spec.json"
    result = attempt / "result.json"

    (old / "stdout.txt").write_text(old_stdout + "\n", encoding="utf-8")
    (new / "stdout.txt").write_text(new_stdout + "\n", encoding="utf-8")
    (old / "stderr.txt").write_text(old_stderr, encoding="utf-8")
    (new / "stderr.txt").write_text(new_stderr, encoding="utf-8")
    (old / "exit_code.txt").write_text(str(old_exit_code) + "\n", encoding="utf-8")
    (new / "exit_code.txt").write_text(str(new_exit_code) + "\n", encoding="utf-8")
    (old / "run.log").write_text("command: python client.py\n", encoding="utf-8")
    (new / "run.log").write_text("command: python client.py\n", encoding="utf-8")
    (old / "build.log").write_text("no build step configured\n", encoding="utf-8")
    (new / "build.log").write_text("no build step configured\n", encoding="utf-8")
    spec.write_text(
        json.dumps(
            {
                "candidate_id": "toy-candidate",
                "library": "toy-drift",
                "old_version": "1.0.0",
                "new_version": "2.0.0",
                "client_file": str(tmp_path / "client.py"),
                "old_environment": _environment("old", "1.0.0"),
                "new_environment": _environment("new", "2.0.0"),
                "comparison_policy": {
                    "ignore_json_fields": [
                        "library_version",
                        "runtime_version",
                    ]
                },
                "schema_version": "1",
                "created_at": "2026-05-22T00:00:00",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    result.write_text(
        json.dumps(
            {
                "candidate_id": "toy-candidate",
                "spec_path": str(spec),
                "attempt_dir": str(attempt),
                "old_run": _run("old", "1.0.0", old, old_exit_code),
                "new_run": _run("new", "2.0.0", new, new_exit_code),
                "diff": {
                    "stdout_changed": old_stdout != new_stdout,
                    "stderr_changed": old_stderr != new_stderr,
                    "exit_code_changed": old_exit_code != new_exit_code,
                    "summary": "stdout changed" if old_stdout != new_stdout else "no observed difference",
                    "details": {},
                },
                "keep": keep,
                "drop_reason": drop_reason,
                "schema_version": "1",
                "created_at": "2026-05-22T00:00:00",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return result


def _environment(label: str, version: str) -> dict:
    return {
        "label": label,
        "library": "toy-drift",
        "version": version,
        "install_command": ["python", "-m", "pip", "install", f"toy-drift=={version}"],
        "python_executable": "python",
        "package_path": None,
    }


def _run(label: str, version: str, root: Path, exit_code: int) -> dict:
    return {
        "label": label,
        "environment": _environment(label, version),
        "stdout_path": str(root / "stdout.txt"),
        "stderr_path": str(root / "stderr.txt"),
        "exit_code_path": str(root / "exit_code.txt"),
        "run_log_path": str(root / "run.log"),
        "build_log_path": str(root / "build.log"),
        "exit_code": exit_code,
        "build_exit_code": None,
    }
