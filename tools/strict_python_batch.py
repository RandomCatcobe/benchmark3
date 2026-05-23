from __future__ import annotations

import argparse
import json
import shutil
import sys
import urllib.request
from dataclasses import dataclass, field
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
class StrictCandidate:
    case_id: str
    slug: str
    title: str
    package: str
    import_name: str
    old: str
    new: str
    source_url: str
    source_excerpt: str
    client: str
    primary_scenario: str
    api_surfaces: list[str]
    drift_patterns: list[str]
    failure_modes: list[str]
    application_scenarios: list[str] = field(default_factory=list)
    extra_packages: list[str] = field(default_factory=list)
    old_extra_packages: list[str] = field(default_factory=list)
    new_extra_packages: list[str] = field(default_factory=list)
    python: str = "3.10"
    review_notes: str = ""
    timeout_s: int = 60
    build_timeout_s: int = 300


COMMON_HEADER = """from __future__ import annotations

import json
"""


CANDIDATES: list[StrictCandidate] = [
    StrictCandidate(
        case_id="PY-STRICT-002",
        slug="python-jinja2-groupby-case-insensitive-default",
        title="Jinja groupby groups case-insensitively by default",
        package="jinja2",
        import_name="jinja2",
        old="3.0.3",
        new="3.1.0",
        source_url="https://jinja.palletsprojects.com/en/stable/changes/#version-3-1-0",
        source_excerpt="Jinja 3.1.0 changed the groupby filter to be case-insensitive by default and added a case_sensitive control.",
        primary_scenario="serialization-and-binding",
        api_surfaces=["template-rendering", "library-api"],
        drift_patterns=["default-changed", "ordering-changed"],
        failure_modes=["silent-value-change", "wrong-order"],
        client=COMMON_HEADER
        + """
from jinja2 import Environment

items = [{"category": "CA"}, {"category": "ca"}, {"category": "NY"}]
template = Environment().from_string(
    '{% for group in items|groupby("category") %}{{ group.grouper }}:{{ group.list|length }};{% endfor %}'
)
print(json.dumps({"rendered": template.render(items=items)}, sort_keys=True))
""",
    ),
    StrictCandidate(
        case_id="PY-STRICT-003",
        slug="python-werkzeug-dump-cookie-path-default",
        title="Werkzeug dump_cookie stops adding Path by default",
        package="werkzeug",
        import_name="werkzeug",
        old="2.2.3",
        new="2.3.0",
        source_url="https://werkzeug.palletsprojects.com/en/stable/changes/#version-2-3-0",
        source_excerpt="Werkzeug 2.3.0 changed cookie handling so dump_cookie no longer sets path='/' by default.",
        primary_scenario="serialization-and-binding",
        api_surfaces=["http-header-serialization", "library-api"],
        drift_patterns=["default-changed", "field-removed-or-masked"],
        failure_modes=["missing-field"],
        client=COMMON_HEADER
        + """
from werkzeug.http import dump_cookie

print(json.dumps({"set_cookie": dump_cookie("sid", "abc")}, sort_keys=True))
""",
    ),
    StrictCandidate(
        case_id="PY-STRICT-004",
        slug="python-starlette-fileresponse-chunk-size-default",
        title="Starlette FileResponse default chunk size increases",
        package="starlette",
        import_name="starlette",
        old="0.17.1",
        new="0.18.0",
        source_url="https://www.starlette.io/release-notes/#0180-january-23-2022",
        source_excerpt="Starlette 0.18.0 changed FileResponse default chunk size from 4 KB to 64 KB.",
        primary_scenario="runtime-semantics",
        api_surfaces=["response-streaming", "library-api"],
        drift_patterns=["default-changed"],
        failure_modes=["silent-value-change"],
        client=COMMON_HEADER
        + """
from pathlib import Path
from starlette.responses import FileResponse

path = Path(__file__)
response = FileResponse(path)
print(json.dumps({"chunk_size": response.chunk_size}, sort_keys=True))
""",
    ),
    StrictCandidate(
        case_id="PY-STRICT-005",
        slug="python-dicttoxml-boolean-text-lowercase",
        title="dicttoxml serializes boolean XML text in lowercase",
        package="dicttoxml",
        import_name="dicttoxml",
        old="1.7.7",
        new="1.7.8",
        source_url="https://raw.githubusercontent.com/quandyfactory/dicttoxml/master/README.md",
        source_excerpt="dicttoxml 1.7.8 changed boolean XML text output from Python True/False to lowercase true/false.",
        primary_scenario="serialization-and-binding",
        api_surfaces=["xml-serialization", "library-api"],
        drift_patterns=["field-semantics-changed"],
        failure_modes=["silent-value-change"],
        python="3.9",
        client=COMMON_HEADER
        + """
from dicttoxml import dicttoxml

text = dicttoxml({"ok": True, "no": False}, attr_type=False, root=False).decode("utf-8")
print(json.dumps({"xml": text}, sort_keys=True))
""",
    ),
    StrictCandidate(
        case_id="PY-STRICT-006",
        slug="python-sanic-keep-alive-timeout-default",
        title="Sanic keep-alive timeout default increases",
        package="sanic",
        import_name="sanic",
        old="23.3.0",
        new="23.6.0",
        source_url="https://sanic.readthedocs.io/en/latest/sanic/changelog.html",
        source_excerpt="Sanic 23.6.0 increased the KEEP_ALIVE_TIMEOUT default.",
        primary_scenario="state-and-lifecycle",
        api_surfaces=["framework-config", "library-api"],
        drift_patterns=["default-changed"],
        failure_modes=["silent-value-change"],
        build_timeout_s=600,
        client=COMMON_HEADER
        + """
from sanic import Sanic

app = Sanic("probe")
print(json.dumps({"keep_alive_timeout": app.config.KEEP_ALIVE_TIMEOUT}, sort_keys=True))
""",
    ),
    StrictCandidate(
        case_id="PY-STRICT-007",
        slug="python-sismic-export-yaml-quote-default",
        title="Sismic export_to_yaml stops quoting by default",
        package="sismic",
        import_name="sismic",
        old="0.26.8",
        new="0.26.9",
        source_url="https://sismic.readthedocs.io/en/1.6.7/changelog.html",
        source_excerpt="Sismic 0.26.9 changed export_to_yaml so it no longer adds quotes by default.",
        primary_scenario="serialization-and-binding",
        api_surfaces=["yaml-serialization", "library-api"],
        drift_patterns=["default-changed"],
        failure_modes=["silent-value-change"],
        extra_packages=["ruamel.yaml==0.17.21"],
        build_timeout_s=600,
        client=COMMON_HEADER
        + r'''
from sismic.io import export_to_yaml, import_from_yaml

statechart = import_from_yaml("""
statechart:
  name: probe
  root state:
    name: root
    initial: idle
    states:
      - name: idle
""")
text = export_to_yaml(statechart)
lines = [line.strip() for line in text.splitlines() if line.strip()]
print(json.dumps({"yaml_lines": lines[:8]}, sort_keys=True))
''',
    ),
    StrictCandidate(
        case_id="PY-STRICT-008",
        slug="python-babel-locale-number-symbols-layout",
        title="Babel Locale number_symbols gains numbering-system layer",
        package="babel",
        import_name="babel",
        old="2.13.1",
        new="2.14.0",
        source_url="https://babel.pocoo.org/en/stable/changelog.html#version-2-14-0",
        source_excerpt="Babel 2.14.0 changed Locale.number_symbols to expose first-level keys for numbering systems such as latn.",
        primary_scenario="time-and-localization",
        api_surfaces=["locale-data", "library-api"],
        drift_patterns=["type-or-shape-changed", "bundled-data-changed"],
        failure_modes=["silent-value-change", "wrong-locale"],
        client=COMMON_HEADER
        + """
from babel.core import Locale

symbols = Locale.parse("en").number_symbols
direct = symbols.get("decimal")
latn = symbols.get("latn")
latn_decimal = latn.get("decimal") if latn is not None else None
print(json.dumps({"direct_decimal": direct, "latn_decimal": latn_decimal, "keys": list(symbols.keys())[:6]}, sort_keys=True))
""",
    ),
    StrictCandidate(
        case_id="PY-STRICT-009",
        slug="python-json-logger-bytes-base64-default",
        title="python-json-logger encodes bytes as URL-safe base64",
        package="python-json-logger",
        import_name="pythonjsonlogger",
        old="3.0.1",
        new="3.1.0",
        source_url="https://nhairs.github.io/python-json-logger/latest/changelog/",
        source_excerpt="python-json-logger 3.1.0 changed the default encoding of bytes values to URL-safe base64.",
        primary_scenario="observability-and-logging",
        api_surfaces=["json-logging", "library-api"],
        drift_patterns=["type-or-shape-changed"],
        failure_modes=["silent-value-change"],
        client=COMMON_HEADER
        + """
import logging
from pythonjsonlogger import jsonlogger

record = logging.LogRecord("probe", logging.INFO, __file__, 1, "hello", (), None)
record.payload = b"abc"
formatter = jsonlogger.JsonFormatter("%(message)s %(payload)s")
payload = json.loads(formatter.format(record))["payload"]
print(json.dumps({"payload": payload}, sort_keys=True))
""",
    ),
    StrictCandidate(
        case_id="PY-STRICT-010",
        slug="python-pygments-htmlformatter-filename-table",
        title="Pygments HtmlFormatter moves filename into a table header",
        package="pygments",
        import_name="pygments",
        old="2.8.1",
        new="2.9.0",
        source_url="https://pygments.org/docs/changelog/#version-2-9-0",
        source_excerpt="Pygments 2.9.0 changed HtmlFormatter table output when filename is provided with table line numbers.",
        primary_scenario="serialization-and-binding",
        api_surfaces=["html-formatting", "library-api"],
        drift_patterns=["type-or-shape-changed"],
        failure_modes=["silent-value-change"],
        client=COMMON_HEADER
        + """
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

html = highlight('print("x")\\n', PythonLexer(), HtmlFormatter(linenos="table", filename="demo.py"))
print(json.dumps({"html": html}, sort_keys=True))
""",
    ),
    StrictCandidate(
        case_id="PY-STRICT-011",
        slug="python-markdown-footnote-reference-order",
        title="Python-Markdown footnotes order by reference occurrence",
        package="markdown",
        import_name="markdown",
        old="3.8.2",
        new="3.9.0",
        source_url="https://python-markdown.github.io/changelog/",
        source_excerpt="Python-Markdown 3.9.0 changed footnote output ordering to follow reference occurrence.",
        primary_scenario="serialization-and-binding",
        api_surfaces=["markdown-rendering", "library-api"],
        drift_patterns=["ordering-changed"],
        failure_modes=["wrong-order"],
        client=COMMON_HEADER
        + r'''
import re
import markdown

text = "B first.[^b] A second.[^a]\n\n[^a]: Alpha\n[^b]: Beta\n"
html = markdown.markdown(text, extensions=["footnotes"])
ids = re.findall(r'id="fn:([^"]+)"', html)
print(json.dumps({"footnote_ids": ids}, sort_keys=True))
''',
    ),
    StrictCandidate(
        case_id="PY-STRICT-012",
        slug="python-loguru-serialized-json-non-ascii",
        title="Loguru serialized JSON stops escaping non-ASCII",
        package="loguru",
        import_name="loguru",
        old="0.5.3",
        new="0.6.0",
        source_url="https://loguru.readthedocs.io/en/latest/project/changelog.html",
        source_excerpt="Loguru 0.6.0 changed serialized JSON output so non-ASCII characters are not escaped by default.",
        primary_scenario="observability-and-logging",
        api_surfaces=["json-logging", "library-api"],
        drift_patterns=["field-semantics-changed"],
        failure_modes=["silent-value-change"],
        client=COMMON_HEADER
        + """
import io
from loguru import logger

stream = io.StringIO()
logger.remove()
logger.add(stream, serialize=True, format="{message}")
logger.info("\\u96ea")
line = stream.getvalue()
print(json.dumps({"contains_escape": "\\\\u96ea" in line, "contains_literal": "\\u96ea" in line}, sort_keys=True))
""",
    ),
    StrictCandidate(
        case_id="PY-STRICT-013",
        slug="python-yarl-url-join-empty-segment",
        title="yarl URL.join preserves empty URL path segment text",
        package="yarl",
        import_name="yarl",
        old="1.9.9",
        new="1.9.10",
        source_url="https://yarl.aio-libs.org/en/stable/changes/",
        source_excerpt="yarl 1.9.10 changed URL.join handling of empty URL path segments.",
        primary_scenario="routing-and-identity",
        api_surfaces=["url-parsing", "library-api"],
        drift_patterns=["parser-rule-changed"],
        failure_modes=["wrong-route"],
        client=COMMON_HEADER
        + """
from yarl import URL

joined = URL("https://web.archive.org/web/").join(URL("./https://github.com/aio-libs/yarl"))
print(json.dumps({"joined": str(joined)}, sort_keys=True))
""",
    ),
    StrictCandidate(
        case_id="PY-STRICT-014",
        slug="python-beautifulsoup-script-get-text",
        title="Beautiful Soup script get_text returns tag-local script text",
        package="beautifulsoup4",
        import_name="bs4",
        old="4.9.3",
        new="4.10.0",
        source_url="https://bugs.launchpad.net/bugs/1906226",
        source_excerpt="Beautiful Soup changed Tag.get_text behavior for direct script tag access while parent text extraction still skips script text.",
        primary_scenario="parsing-and-ingestion",
        api_surfaces=["html-parsing", "library-api"],
        drift_patterns=["field-semantics-changed"],
        failure_modes=["missing-field"],
        client=COMMON_HEADER
        + """
from bs4 import BeautifulSoup

html = "<div><script>var token = 1;</script><p>Hello</p></div>"
soup = BeautifulSoup(html, "html.parser")
print(json.dumps({"script_text": soup.script.get_text(), "div_text": soup.div.get_text("|")}, sort_keys=True))
""",
    ),
    StrictCandidate(
        case_id="PY-STRICT-015",
        slug="python-coverage-json-docstring-executed-lines",
        title="coverage JSON report stops counting module docstrings as executed",
        package="coverage",
        import_name="coverage",
        old="7.13.0",
        new="7.13.1",
        source_url="https://coverage.readthedocs.io/en/latest/changes.html#version-7-13-1-2025-12-28",
        source_excerpt="coverage 7.13.1 changed JSON executed_lines so module docstrings are no longer counted as executed lines.",
        primary_scenario="observability-and-logging",
        api_surfaces=["coverage-reporting", "library-api"],
        drift_patterns=["field-semantics-changed"],
        failure_modes=["silent-value-change"],
        client=COMMON_HEADER
        + """
import tempfile
import runpy
from pathlib import Path
import coverage

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    module = root / "probe_module.py"
    module.write_text('\"\"\"module docs\"\"\"\\nvalue = 42\\n', encoding="utf-8")
    cov = coverage.Coverage(data_file=str(root / ".coverage"))
    cov.start()
    runpy.run_path(str(module))
    cov.stop()
    cov.save()
    report = root / "coverage.json"
    cov.json_report(outfile=str(report), include=[str(module)])
    data = json.loads(report.read_text(encoding="utf-8"))
    file_data = next(iter(data["files"].values()))
print(json.dumps({"executed_lines": file_data["executed_lines"], "summary": file_data["summary"]}, sort_keys=True))
""",
    ),
    StrictCandidate(
        case_id="PY-STRICT-016",
        slug="python-json5-int-subclass-serialization",
        title="json5 int subclass serialization stops using custom str",
        package="json5",
        import_name="json5",
        old="0.9.8",
        new="0.9.9",
        source_url="https://github.com/dpranke/pyjson5",
        source_excerpt="json5 0.9.9 fixed serialization of int subclasses so numeric output no longer comes from custom __str__ text.",
        primary_scenario="serialization-and-binding",
        api_surfaces=["json5-serialization", "library-api"],
        drift_patterns=["field-semantics-changed"],
        failure_modes=["silent-value-change"],
        client=COMMON_HEADER
        + """
import json5

class OddInt(int):
    def __str__(self) -> str:
        return "not-json5-number"

print(json.dumps({"text": json5.dumps({"n": OddInt(7)})}, sort_keys=True))
""",
    ),
    StrictCandidate(
        case_id="PY-STRICT-017",
        slug="python-filelock-import-logger-level",
        title="filelock no longer sets package logger level on import",
        package="filelock",
        import_name="filelock",
        old="3.3.0",
        new="3.3.1",
        source_url="https://py-filelock.readthedocs.io/en/latest/changelog.html#v3-3-1-2021-10-15",
        source_excerpt="filelock 3.3.1 stopped setting the filelock logger level during import.",
        primary_scenario="observability-and-logging",
        api_surfaces=["logging-configuration", "library-api"],
        drift_patterns=["default-changed"],
        failure_modes=["silent-value-change"],
        client=COMMON_HEADER
        + """
import logging

logging.basicConfig(level=logging.INFO, force=True)
import filelock  # noqa: F401,E402

logger = logging.getLogger("filelock")
print(json.dumps({"level": logger.level, "effective_level": logger.getEffectiveLevel(), "debug_enabled": logger.isEnabledFor(logging.DEBUG)}, sort_keys=True))
""",
    ),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append", default=[])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--venv-root", default=str(Path("D:/sdv")))
    args = parser.parse_args()

    selected = [item for item in CANDIDATES if not args.only or item.slug in args.only or item.case_id in args.only]
    if args.limit is not None:
        selected = selected[: args.limit]

    py310 = ROOT / ".uv-python" / "cpython-3.10.20-windows-x86_64-none" / "python.exe"
    py39 = Path.home() / "AppData" / "Roaming" / "uv" / "python" / "cpython-3.9.25-windows-x86_64-none" / "python.exe"
    python_by_key = {"3.10": py310, "3.9": py39}

    created = 0
    skipped = 0
    failed = 0
    for candidate in selected:
        print(f"== {candidate.case_id} {candidate.slug}")
        package_dir = ROOT / "docs" / "case-bank" / "cases" / candidate.primary_scenario / candidate.slug
        if package_dir.exists() and not args.force:
            print(f"skip existing {package_dir}")
            skipped += 1
            continue
        try:
            _run_one(candidate, python_by_key[candidate.python], Path(args.venv_root), force=args.force)
        except Exception as exc:
            print(f"FAIL {candidate.slug}: {exc}")
            failed += 1
            continue
        created += 1
    print(json.dumps({"created": created, "skipped": skipped, "failed": failed}, sort_keys=True))
    return 0 if failed == 0 else 1


def _run_one(candidate: StrictCandidate, python_executable: Path, venv_root: Path, force: bool) -> None:
    if not python_executable.exists():
        raise RuntimeError(f"missing Python executable: {python_executable}")
    if _major(candidate.old) != _major(candidate.new):
        raise RuntimeError(f"major version changed: {candidate.old} -> {candidate.new}")
    _assert_not_yanked(candidate.package, candidate.old)
    _assert_not_yanked(candidate.package, candidate.new)

    artifact_root = ROOT / "data" / "verification" / "strict_python" / candidate.slug
    if artifact_root.exists() and force:
        shutil.rmtree(artifact_root)
    artifact_root.mkdir(parents=True, exist_ok=True)
    client_path = artifact_root / "client.py"
    candidate_path = artifact_root / "candidate.json"
    client_path.write_text(candidate.client.strip() + "\n", encoding="utf-8")
    candidate_payload = {
        "case_id": candidate.slug.replace("-", "_"),
        "candidate_id": candidate.slug,
        "library": candidate.package,
        "ecosystem": "python",
        "version_old": candidate.old,
        "version_new": candidate.new,
        "confidence": "high",
        "api_surface": candidate.api_surfaces,
        "source_url": candidate.source_url,
        "source_type": "release_notes",
        "retrieved_at": "2026-05-23",
        "excerpt": candidate.source_excerpt,
        "review_notes": candidate.review_notes or "Strict batch: same public call shape, both sides exit 0, runtime stderr must stay empty.",
        "drift_patterns": candidate.drift_patterns,
        "failure_modes": candidate.failure_modes,
    }
    candidate_path.write_text(json.dumps(candidate_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    spec = create_reproduction_spec(
        candidate_id=candidate.slug,
        library=candidate.package,
        old_version=candidate.old,
        new_version=candidate.new,
        client_file=client_path,
        old_python_executable=str(python_executable),
        new_python_executable=str(python_executable),
        extra_packages=candidate.extra_packages,
        old_extra_packages=candidate.old_extra_packages,
        new_extra_packages=candidate.new_extra_packages,
        ignore_json_fields=["library_version", "package_version", "version"],
    )
    result = run_reproduction_spec(
        spec,
        artifact_root,
        timeout_s=candidate.timeout_s,
        install=True,
        venv_root=venv_root,
        build_timeout_s=candidate.build_timeout_s,
    )
    _assert_clean_result(result)
    create_case_bank_package(
        CaseBankPackageRequest(
            reproduction_result=Path(result.attempt_dir) / "result.json",
            candidate=candidate_path,
            client=client_path,
            out_root=ROOT / "docs" / "case-bank" / "cases",
            primary_scenario=candidate.primary_scenario,
            case_id=candidate.case_id,
            slug=candidate.slug,
            title=candidate.title,
            status="verified_keep",
            source_urls=[candidate.source_url],
            source_excerpt=candidate.source_excerpt,
            retrieved_at="2026-05-23",
            ecosystem="python",
            languages=["python"],
            api_surfaces=candidate.api_surfaces,
            application_scenarios=candidate.application_scenarios or [candidate.primary_scenario],
            drift_patterns=candidate.drift_patterns,
            failure_modes=candidate.failure_modes,
            determinism="local-deterministic",
            external_dependencies="package-cache",
            review_notes=candidate.review_notes or "Generated by strict Python batch after clean old/new local reproduction.",
            overwrite=force,
        )
    )


def _major(version: str) -> str:
    return version.split(".", 1)[0]


_PYPI_CACHE: dict[str, dict] = {}


def _pypi_payload(package: str) -> dict:
    if package not in _PYPI_CACHE:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{package}/json", timeout=30) as response:
            _PYPI_CACHE[package] = json.loads(response.read().decode("utf-8"))
    return _PYPI_CACHE[package]


def _assert_not_yanked(package: str, version: str) -> None:
    payload = _pypi_payload(package)
    files = payload.get("releases", {}).get(version)
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
