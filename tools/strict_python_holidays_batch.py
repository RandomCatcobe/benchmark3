from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "silent_drift_miner" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from silent_drift_miner.case_bank_writer import (  # noqa: E402
    CaseBankPackageRequest,
    create_case_bank_package,
)
from silent_drift_miner.reproduction import (  # noqa: E402
    create_reproduction_spec,
    run_reproduction_spec,
)


@dataclass(frozen=True)
class HolidayCase:
    case_id: str
    slug: str
    old: str
    new: str
    country: str
    date: str
    title: str


CASES: list[HolidayCase] = [
    HolidayCase("PY-HOL-001", "python-holidays-ae-arafat-day-name", "0.28", "0.29", "AE", "2020-07-30", "holidays changes United Arab Emirates Arafat Day label"),
    HolidayCase("PY-HOL-002", "python-holidays-be-new-year-locale", "0.28", "0.29", "BE", "2020-01-01", "holidays changes Belgium New Year holiday label"),
    HolidayCase("PY-HOL-003", "python-holidays-bf-eid-estimate-marker", "0.28", "0.29", "BF", "2023-06-28", "holidays changes Burkina Faso Eid al-Adha estimate marker"),
    HolidayCase("PY-HOL-004", "python-holidays-bg-good-friday-label", "0.28", "0.29", "BG", "2020-04-17", "holidays changes Bulgaria Good Friday label"),
    HolidayCase("PY-HOL-005", "python-holidays-bh-labor-day-spelling", "0.28", "0.29", "BH", "2020-05-01", "holidays changes Bahrain Labor Day spelling"),
    HolidayCase("PY-HOL-006", "python-holidays-cm-eid-estimate-marker", "0.28", "0.29", "CM", "2023-06-28", "holidays changes Cameroon Eid al-Adha estimate marker"),
    HolidayCase("PY-HOL-007", "python-holidays-cz-restoration-day-label", "0.28", "0.29", "CZ", "2020-01-01", "holidays changes Czech restoration day label"),
    HolidayCase("PY-HOL-008", "python-holidays-dz-labor-day-spelling", "0.28", "0.29", "DZ", "2020-05-01", "holidays changes Algeria Labor Day spelling"),
    HolidayCase("PY-HOL-009", "python-holidays-eg-bank-new-year-label", "0.28", "0.29", "EG", "2020-01-01", "holidays changes Egypt New Year bank holiday label"),
    HolidayCase("PY-HOL-010", "python-holidays-ga-eid-estimate-marker", "0.28", "0.29", "GA", "2023-06-28", "holidays changes Gabon Eid al-Adha estimate marker"),
    HolidayCase("PY-HOL-011", "python-holidays-gt-new-year-added", "0.28", "0.29", "GT", "2020-01-01", "holidays adds Guatemala New Year holiday"),
    HolidayCase("PY-HOL-012", "python-holidays-hr-new-year-label", "0.28", "0.29", "HR", "2020-01-01", "holidays changes Croatia New Year label"),
    HolidayCase("PY-HOL-013", "python-holidays-lu-new-year-label", "0.28", "0.29", "LU", "2020-01-01", "holidays changes Luxembourg New Year label"),
    HolidayCase("PY-HOL-014", "python-holidays-ma-new-year-label", "0.28", "0.29", "MA", "2020-01-01", "holidays changes Morocco New Year label"),
    HolidayCase("PY-HOL-015", "python-holidays-my-hari-raya-haji-removed", "0.28", "0.29", "MY", "2023-06-28", "holidays changes Malaysia Hari Raya Haji entry"),
    HolidayCase("PY-HOL-016", "python-holidays-pk-eid-ul-fitr-removed", "0.28", "0.29", "PK", "2023-04-21", "holidays changes Pakistan Eid-ul-Fitr entry"),
    HolidayCase("PY-HOL-017", "python-holidays-ru-christmas-label", "0.28", "0.29", "RU", "2020-01-07", "holidays changes Russia Christmas label"),
    HolidayCase("PY-HOL-018", "python-holidays-sa-arafat-day-label", "0.28", "0.29", "SA", "2020-07-30", "holidays changes Saudi Arabia Arafat Day label"),
    HolidayCase("PY-HOL-019", "python-holidays-si-new-year-label", "0.28", "0.29", "SI", "2020-01-01", "holidays changes Slovenia New Year label"),
    HolidayCase("PY-HOL-020", "python-holidays-td-eid-estimate-marker", "0.28", "0.29", "TD", "2023-06-28", "holidays changes Chad Eid al-Adha estimate marker"),
    HolidayCase("PY-HOL-021", "python-holidays-tn-revolution-day-label", "0.28", "0.29", "TN", "2020-01-14", "holidays changes Tunisia Revolution and Youth Day label"),
    HolidayCase("PY-HOL-022", "python-holidays-ao-new-year-label", "0.29", "0.30", "AO", "2020-01-01", "holidays changes Angola New Year label"),
    HolidayCase("PY-HOL-023", "python-holidays-bo-new-year-label", "0.29", "0.30", "BO", "2020-01-01", "holidays changes Bolivia New Year label"),
    HolidayCase("PY-HOL-024", "python-holidays-dj-new-year-label", "0.29", "0.30", "DJ", "2020-01-01", "holidays changes Djibouti New Year label"),
    HolidayCase("PY-HOL-025", "python-holidays-ge-christmas-label", "0.29", "0.30", "GE", "2020-01-07", "holidays changes Georgia Christmas label"),
    HolidayCase("PY-HOL-026", "python-holidays-gr-apostrophe-normalization", "0.29", "0.30", "GR", "2020-01-01", "holidays normalizes Greece New Year's Day punctuation"),
    HolidayCase("PY-HOL-027", "python-holidays-id-new-year-label", "0.29", "0.30", "ID", "2020-01-01", "holidays changes Indonesia New Year label"),
    HolidayCase("PY-HOL-028", "python-holidays-kr-lunar-new-year-eve-label", "0.29", "0.30", "KR", "2020-01-24", "holidays changes Korea Lunar New Year eve label"),
    HolidayCase("PY-HOL-029", "python-holidays-mz-fraternalism-label", "0.29", "0.30", "MZ", "2020-01-01", "holidays changes Mozambique January holiday label"),
    HolidayCase("PY-HOL-030", "python-holidays-th-bridge-public-holiday-added", "0.29", "0.30", "TH", "2023-07-31", "holidays adds Thailand bridge public holiday"),
    HolidayCase("PY-HOL-031", "python-holidays-tw-founding-day-label", "0.29", "0.30", "TW", "2020-01-01", "holidays changes Taiwan founding day label"),
    HolidayCase("PY-HOL-032", "python-holidays-ua-substituted-day-added", "0.29", "0.30", "UA", "2020-01-06", "holidays adds Ukraine substituted day off"),
    HolidayCase("PY-HOL-033", "python-holidays-uy-childrens-day-removed", "0.29", "0.30", "UY", "2020-01-06", "holidays changes Uruguay Children's Day entry"),
    HolidayCase("PY-HOL-034", "python-holidays-bb-new-year-added", "0.30", "0.31", "BB", "2020-01-01", "holidays adds Barbados New Year holiday"),
    HolidayCase("PY-HOL-035", "python-holidays-ir-fatima-martyrdom-added", "0.30", "0.31", "IR", "2020-01-28", "holidays adds Iran Martyrdom of Fatima holiday"),
    HolidayCase("PY-HOL-036", "python-holidays-sg-polling-day-added", "0.30", "0.31", "SG", "2023-09-01", "holidays adds Singapore Polling Day"),
    HolidayCase("PY-HOL-037", "python-holidays-si-solidarity-day-added", "0.30", "0.31", "SI", "2023-08-14", "holidays adds Slovenia Solidarity Day"),
    HolidayCase("PY-HOL-038", "python-holidays-vu-new-year-added", "0.30", "0.31", "VU", "2020-01-01", "holidays adds Vanuatu New Year holiday"),
    HolidayCase("PY-HOL-039", "python-holidays-sa-eid-observed-estimate-label", "0.30", "0.31", "SA", "2020-08-03", "holidays changes Saudi Arabia Eid observed label"),
    HolidayCase("PY-HOL-040", "python-holidays-ae-islamic-new-year-label", "0.28", "0.29", "AE", "2020-08-23", "holidays changes United Arab Emirates Islamic New Year label"),
    HolidayCase("PY-HOL-041", "python-holidays-ae-national-day-holiday-label", "0.28", "0.29", "AE", "2020-12-03", "holidays changes United Arab Emirates National Day holiday label"),
    HolidayCase("PY-HOL-042", "python-holidays-be-easter-label", "0.28", "0.29", "BE", "2020-04-12", "holidays changes Belgium Easter label"),
    HolidayCase("PY-HOL-043", "python-holidays-be-labor-day-label", "0.28", "0.29", "BE", "2020-05-01", "holidays changes Belgium Labor Day label"),
    HolidayCase("PY-HOL-044", "python-holidays-bh-ashura-eve-label", "0.28", "0.29", "BH", "2020-08-28", "holidays changes Bahrain Ashura Eve label"),
    HolidayCase("PY-HOL-045", "python-holidays-bh-prophet-birthday-label", "0.28", "0.29", "BH", "2020-10-29", "holidays changes Bahrain Prophet birthday label"),
    HolidayCase("PY-HOL-046", "python-holidays-ru-new-year-christmas-holiday-label", "0.28", "0.29", "RU", "2020-01-01", "holidays changes Russia New Year holiday label"),
    HolidayCase("PY-HOL-047", "python-holidays-tn-martyrs-day-label", "0.28", "0.29", "TN", "2020-04-09", "holidays changes Tunisia Martyrs Day label"),
]


KEEP_HOLIDAY_CASE_IDS = {
    "PY-HOL-015",  # value -> null
    "PY-HOL-026",  # label normalization
    "PY-HOL-036",  # null -> value
}

HOLIDAY_CLUSTER_REJECTION_NOTE = (
    "Clean reproduction, but rejected during curation because the holidays cluster is already "
    "represented by PY-HOL-015, PY-HOL-026, and PY-HOL-036. Keeping more same-upstream "
    "bundled-calendar data slices would overweight one package and weaken benchmark diversity."
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append", default=[])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--venv-root", default="D:/sdv/holidays")
    args = parser.parse_args()

    selected = [case for case in CASES if not args.only or case.case_id in args.only or case.slug in args.only]
    if args.limit is not None:
        selected = selected[: args.limit]

    py310 = ROOT / ".uv-python" / "cpython-3.10.20-windows-x86_64-none" / "python.exe"
    venv_root = Path(args.venv_root)
    created = 0
    failed = 0
    skipped = 0
    for case in selected:
        print(f"== {case.case_id} {case.slug}", flush=True)
        package_dir = ROOT / "docs" / "case-bank" / "cases" / "time-and-localization" / case.slug
        if package_dir.exists() and not args.force:
            print(f"skip existing {package_dir}", flush=True)
            skipped += 1
            continue
        try:
            _run_one(case, py310, venv_root, force=args.force)
        except Exception as exc:
            print(f"FAIL {case.slug}: {exc}", flush=True)
            failed += 1
            continue
        created += 1
    print(json.dumps({"created": created, "failed": failed, "skipped": skipped}, sort_keys=True), flush=True)
    return 0 if failed == 0 else 1


def _run_one(case: HolidayCase, base_python: Path, venv_root: Path, force: bool) -> None:
    _assert_not_yanked("holidays", case.old)
    _assert_not_yanked("holidays", case.new)
    old_python = _ensure_env(base_python, venv_root, case.old)
    new_python = _ensure_env(base_python, venv_root, case.new)

    artifact_root = ROOT / "data" / "verification" / "strict_python_holidays" / case.slug
    if artifact_root.exists() and force:
        shutil.rmtree(artifact_root)
    artifact_root.mkdir(parents=True, exist_ok=True)
    client_path = artifact_root / "client.py"
    candidate_path = artifact_root / "candidate.json"
    year = case.date.split("-", 1)[0]
    client_path.write_text(
        "\n".join(
            [
                "from __future__ import annotations",
                "",
                "import json",
                "import holidays",
                "",
                f"country = {case.country!r}",
                f"date = {case.date!r}",
                f"calendar = holidays.country_holidays(country, years=[{year}])",
                "print(json.dumps({'country': country, 'date': date, 'holiday': calendar.get(date)}, sort_keys=True))",
                "",
            ]
        ),
        encoding="utf-8",
    )
    source_url = f"https://github.com/vacanza/holidays/releases/tag/v{case.new}"
    source_excerpt = "The holidays release updates bundled country holiday definitions while preserving the country_holidays API."
    candidate_path.write_text(
        json.dumps(
            {
                "case_id": case.slug.replace("-", "_"),
                "candidate_id": case.slug,
                "library": "holidays",
                "ecosystem": "python",
                "version_old": case.old,
                "version_new": case.new,
                "confidence": "high",
                "api_surface": ["holiday-calendar-data", "library-api"],
                "source_url": source_url,
                "source_type": "release_notes",
                "retrieved_at": "2026-05-23",
                "excerpt": source_excerpt,
                "review_notes": "Strict holidays batch: same country_holidays call, adjacent 0.x release, both sides exit 0, stderr must stay empty.",
                "drift_patterns": ["bundled-data-changed"],
                "failure_modes": ["silent-value-change"],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    spec = create_reproduction_spec(
        candidate_id=case.slug,
        library="holidays",
        old_version=case.old,
        new_version=case.new,
        client_file=client_path,
        old_python_executable=str(old_python),
        new_python_executable=str(new_python),
        ignore_json_fields=["library_version", "package_version", "version"],
    )
    result = run_reproduction_spec(spec, artifact_root, timeout_s=30, install=False)
    _assert_clean_result(result)
    status = "verified_keep" if case.case_id in KEEP_HOLIDAY_CASE_IDS else "rejected_cluster_duplicate"
    review_notes = (
        "Kept as one of three representative holidays bundled-data drift shapes."
        if status == "verified_keep"
        else HOLIDAY_CLUSTER_REJECTION_NOTE
    )
    package_dir = create_case_bank_package(
        CaseBankPackageRequest(
            reproduction_result=Path(result.attempt_dir) / "result.json",
            candidate=candidate_path,
            client=client_path,
            out_root=ROOT / "docs" / "case-bank" / "cases",
            primary_scenario="time-and-localization",
            case_id=case.case_id,
            slug=case.slug,
            title=case.title,
            status=status,
            source_urls=[source_url],
            source_excerpt=source_excerpt,
            retrieved_at="2026-05-23",
            ecosystem="python",
            languages=["python"],
            api_surfaces=["holiday-calendar-data", "library-api"],
            application_scenarios=["time-and-localization"],
            drift_patterns=["bundled-data-changed"],
            failure_modes=["silent-value-change"],
            determinism="local-deterministic",
            external_dependencies="package-cache",
            review_notes=review_notes,
            overwrite=force,
        )
    )
    _annotate_curation_decision(package_dir, status)


def _annotate_curation_decision(package_dir: Path, status: str) -> None:
    metadata_path = package_dir / "metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    provenance = metadata.setdefault("provenance", {})
    if status == "verified_keep":
        provenance["curation_decision"] = "kept_representative_holidays_case"
        provenance["curation_reason"] = (
            "Kept as one of three holidays representatives: value-to-null removal, "
            "label normalization, and null-to-value addition."
        )
    else:
        provenance["curation_status_before_rebalance"] = "verified_keep"
        provenance["curation_decision"] = "rejected_cluster_duplicate"
        provenance["curation_rejected_at"] = "2026-05-23"
        provenance["curation_reason"] = HOLIDAY_CLUSTER_REJECTION_NOTE
        provenance["kept_representatives"] = sorted(KEEP_HOLIDAY_CASE_IDS)
        case_path = package_dir / "case.md"
        case_path.write_text(
            case_path.read_text(encoding="utf-8").rstrip()
            + "\n\n## Why This Was Not Kept\n\n"
            + "This case is a clean silent-drift reproduction, not a failed replay. It was moved to the rejected side "
            + "because `PY-HOL-015`, `PY-HOL-026`, and `PY-HOL-036` already cover the representative `holidays` drift "
            + "shapes. Additional same-upstream calendar-data slices are too clustered for the keep set.\n",
            encoding="utf-8",
        )
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _ensure_env(base_python: Path, root: Path, version: str) -> Path:
    env = root / f"holidays-{version}"
    python = env / "Scripts" / "python.exe"
    if not python.exists():
        env.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([str(base_python), "-m", "venv", str(env)], check=True)
    probe = subprocess.run(
        [str(python), "-c", "import holidays, sys; sys.exit(0 if holidays.__version__ == sys.argv[1] else 1)", version],
        capture_output=True,
        text=True,
        check=False,
    )
    if probe.returncode != 0:
        subprocess.run([str(python), "-m", "pip", "install", "-q", f"holidays=={version}"], check=True)
    return python


_PYPI_CACHE: dict[str, dict] = {}


def _pypi_payload(package: str) -> dict:
    if package not in _PYPI_CACHE:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{package}/json", timeout=30) as response:
            _PYPI_CACHE[package] = json.loads(response.read().decode("utf-8"))
    return _PYPI_CACHE[package]


def _assert_not_yanked(package: str, version: str) -> None:
    files = _pypi_payload(package).get("releases", {}).get(version)
    if not files:
        raise RuntimeError(f"{package}=={version} not found on PyPI")
    if all(file.get("yanked", False) for file in files):
        raise RuntimeError(f"{package}=={version} is yanked")


def _assert_clean_result(result) -> None:
    if not result.keep:
        raise RuntimeError(f"not kept: {result.drop_reason} {result.diff.summary}")
    if result.old_run.exit_code != 0 or result.new_run.exit_code != 0:
        raise RuntimeError(f"nonzero exit: old={result.old_run.exit_code} new={result.new_run.exit_code}")
    old_stderr = Path(result.old_run.stderr_path).read_text(encoding="utf-8").strip()
    new_stderr = Path(result.new_run.stderr_path).read_text(encoding="utf-8").strip()
    if old_stderr or new_stderr:
        raise RuntimeError(f"runtime stderr not empty: old={old_stderr[:200]!r} new={new_stderr[:200]!r}")
    if not result.diff.stdout_changed:
        raise RuntimeError(f"stdout did not change: {result.diff.summary}")


if __name__ == "__main__":
    raise SystemExit(main())
