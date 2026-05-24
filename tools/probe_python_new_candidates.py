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
class Candidate:
    case_id: str
    slug: str
    title: str
    package: str
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
    python: str = "3.10"
    timeout_s: int = 60
    build_timeout_s: int = 300


HEADER = """from __future__ import annotations

import json
"""


CANDIDATES = [
    Candidate(
        case_id="PY-STRICT-018",
        slug="python-urllib3-httpconnection-blocksize-default",
        title="urllib3 HTTPConnection blocksize default doubles",
        package="urllib3",
        old="2.0.4",
        new="2.0.5",
        source_url="https://urllib3.readthedocs.io/en/2.0.7/changelog.html",
        source_excerpt="urllib3 2.0.5 increased the default HTTPConnection blocksize.",
        primary_scenario="runtime-semantics",
        api_surfaces=["http-client", "library-api"],
        drift_patterns=["default-changed", "field-semantics-changed"],
        failure_modes=["silent-value-change"],
        client=HEADER
        + """
from urllib3.connection import HTTPConnection

conn = HTTPConnection("example.com")
print(json.dumps({"blocksize": conn.blocksize}, sort_keys=True))
""",
    ),
    Candidate(
        case_id="PY-STRICT-019",
        slug="python-email-validator-display-name-nfc",
        title="email-validator normalizes display names to NFC",
        package="email-validator",
        old="2.2.0",
        new="2.3.0",
        source_url="https://pypi.org/project/email-validator/2.3.0/",
        source_excerpt="email-validator 2.3.0 normalizes display names returned by validate_email.",
        primary_scenario="validation-and-policy",
        api_surfaces=["email-validation", "library-api"],
        drift_patterns=["field-semantics-changed"],
        failure_modes=["silent-value-change"],
        client=HEADER
        + r'''
import unicodedata
from email_validator import validate_email

result = validate_email('"Cafe\u0301" <me@example.com>', allow_display_name=True, check_deliverability=False)
name = result.display_name
print(json.dumps({"display_name": name, "is_nfc": unicodedata.is_normalized("NFC", name)}, sort_keys=True))
''',
    ),
    Candidate(
        case_id="PY-STRICT-020",
        slug="python-chardet-koi8r-cookie-detection",
        title="chardet detects KOI8-R coding cookies",
        package="chardet",
        old="7.0.0",
        new="7.1.0",
        source_url="https://chardet.readthedocs.io/en/latest/changelog.html",
        source_excerpt="chardet 7.1.0 improved detection for Python coding cookies.",
        primary_scenario="parsing-and-ingestion",
        api_surfaces=["encoding-detection", "library-api"],
        drift_patterns=["parser-rule-changed", "field-semantics-changed"],
        failure_modes=["silent-value-change", "wrong-locale"],
        client=HEADER
        + r'''
import chardet

detected = chardet.detect(b"# -*- coding: koi8-r -*-\nprint('x')\n")
print(json.dumps({"encoding": detected.get("encoding"), "confidence": detected.get("confidence")}, sort_keys=True))
''',
    ),
    Candidate(
        case_id="PY-STRICT-021",
        slug="python-pathspec-gitignore-negated-directory-file",
        title="pathspec GitIgnoreSpec unignores files under negated directories",
        package="pathspec",
        old="0.11.2",
        new="0.12.1",
        source_url="https://pypi.org/project/pathspec/0.12.1/",
        source_excerpt="pathspec 0.12.x fixed GitIgnoreSpec matching for negated files below ignored directories.",
        primary_scenario="parsing-and-ingestion",
        api_surfaces=["gitignore-matching", "library-api"],
        drift_patterns=["parser-rule-changed", "validation-relaxed"],
        failure_modes=["silent-acceptance-change", "silent-value-change"],
        client=HEADER
        + """
from pathspec.gitignore import GitIgnoreSpec

spec = GitIgnoreSpec.from_lines(["subdir/", "!subdir/file.txt"])
print(json.dumps({"ignored": spec.match_file("subdir/file.txt")}, sort_keys=True))
""",
    ),
    Candidate(
        case_id="PY-STRICT-022",
        slug="python-marshmallow-schema-method-name-field",
        title="marshmallow preserves Schema.dump when field has the same name",
        package="marshmallow",
        old="3.12.1",
        new="3.12.2",
        source_url="https://marshmallow.readthedocs.io/en/stable/changelog.html",
        source_excerpt="marshmallow 3.12.2 restored behavior when a declared field name collides with a Schema method name.",
        primary_scenario="serialization-and-binding",
        api_surfaces=["schema-serialization", "library-api"],
        drift_patterns=["field-semantics-changed"],
        failure_modes=["silent-value-change"],
        client=HEADER
        + """
from marshmallow import Schema, fields

class ProbeSchema(Schema):
    dump = fields.String()

schema = ProbeSchema()
print(json.dumps({"dump_callable": callable(schema.dump), "fields": sorted(schema.fields)}, sort_keys=True))
""",
    ),
    Candidate(
        case_id="PY-STRICT-023",
        slug="python-dotenv-override-expansion-order",
        title="python-dotenv expands variables using override precedence",
        package="python-dotenv",
        old="0.15.0",
        new="0.16.0",
        source_url="https://bbc2.github.io/python-dotenv/changelog/",
        source_excerpt="python-dotenv 0.16.0 changed variable expansion so override=False respects environment precedence.",
        primary_scenario="state-and-lifecycle",
        api_surfaces=["environment-loading", "library-api"],
        drift_patterns=["default-changed", "field-semantics-changed"],
        failure_modes=["stale-state", "silent-value-change"],
        client=HEADER
        + r'''
import os
from io import StringIO
from dotenv import dotenv_values

os.environ["A"] = "env"
values = dotenv_values(stream=StringIO("A=file\nB=${A}\n"), interpolate=True)
print(json.dumps({"A": values.get("A"), "B": values.get("B")}, sort_keys=True))
''',
    ),
    Candidate(
        case_id="PY-STRICT-024",
        slug="python-slugify-unicode-regex-emoji",
        title="python-slugify applies regex pattern after unicode preservation",
        package="python-slugify",
        old="6.0.0",
        new="6.0.1",
        source_url="https://github.com/un33k/python-slugify/releases/tag/v6.0.1",
        source_excerpt="python-slugify 6.0.1 fixed custom regex pattern handling when allow_unicode is enabled.",
        primary_scenario="serialization-and-binding",
        api_surfaces=["text-normalization", "library-api"],
        drift_patterns=["parser-rule-changed", "field-semantics-changed"],
        failure_modes=["silent-value-change"],
        client=HEADER
        + '''
from slugify import slugify

value = slugify("i love 🦄", allow_unicode=True, regex_pattern=r"[^🦄]+")
print(json.dumps({"slug": value}, sort_keys=True))
''',
    ),
    Candidate(
        case_id="PY-STRICT-025",
        slug="python-feedparser-author-uri-xml-base",
        title="feedparser resolves author URI against xml:base",
        package="feedparser",
        old="6.0.10",
        new="6.0.11",
        source_url="https://feedparser.readthedocs.io/en/latest/changelog/",
        source_excerpt="feedparser 6.0.11 fixed relative URL resolution for selected feed fields.",
        primary_scenario="parsing-and-ingestion",
        api_surfaces=["feed-parsing", "library-api"],
        drift_patterns=["parser-rule-changed", "field-semantics-changed"],
        failure_modes=["wrong-route", "silent-value-change"],
        client=HEADER
        + r'''
import feedparser

feed = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:base="http://example.org/base/">
  <title>Probe</title>
  <author><name>A</name><uri>../people/a</uri></author>
  <entry><title>E</title><id>1</id></entry>
</feed>
"""
parsed = feedparser.parse(feed)
author = parsed.feed.get("author_detail", {})
print(json.dumps({"href": author.get("href") or author.get("uri"), "keys": sorted(author.keys())}, sort_keys=True))
''',
    ),
    Candidate(
        case_id="PY-STRICT-026",
        slug="python-tzdata-asia-choibalsan-2007-offset",
        title="tzdata changes Asia/Choibalsan historical offset",
        package="tzdata",
        old="2024.1",
        new="2024.2",
        source_url="https://github.com/python/tzdata/releases/tag/2024.2",
        source_excerpt="tzdata 2024.2 updates bundled IANA time zone data.",
        primary_scenario="time-and-localization",
        api_surfaces=["timezone-data", "standard-library-adapter"],
        drift_patterns=["bundled-data-changed"],
        failure_modes=["wrong-timezone", "silent-value-change"],
        client=HEADER
        + '''
from datetime import datetime
from zoneinfo import ZoneInfo, reset_tzpath

reset_tzpath([])
dt = datetime(2007, 1, 1, 12, 0, tzinfo=ZoneInfo("Asia/Choibalsan"))
print(json.dumps({"offset_seconds": int(dt.utcoffset().total_seconds())}, sort_keys=True))
''',
    ),
    Candidate(
        case_id="PY-STRICT-027",
        slug="python-scipy-mannwhitneyu-default-method-pvalue",
        title="SciPy mannwhitneyu default method changes p-value",
        package="scipy",
        old="1.6.3",
        new="1.7.3",
        source_url="https://docs.scipy.org/doc/scipy-1.7.0/release.1.7.0.html",
        source_excerpt="SciPy 1.7.0 changed mannwhitneyu behavior by adding method selection for exact and asymptotic p-values.",
        primary_scenario="runtime-semantics",
        api_surfaces=["statistics-api", "library-api"],
        drift_patterns=["default-changed", "field-semantics-changed"],
        failure_modes=["silent-value-change"],
        extra_packages=["numpy==1.21.6"],
        python="3.9",
        timeout_s=120,
        build_timeout_s=600,
        client=HEADER
        + '''
from scipy import stats

result = stats.mannwhitneyu([1, 2, 3], [4, 5, 6])
print(json.dumps({"statistic": float(result.statistic), "pvalue": float(result.pvalue)}, sort_keys=True))
''',
    ),
    Candidate(
        case_id="PY-STRICT-028",
        slug="python-markdown-footnotes-reference-order",
        title="Python-Markdown orders footnotes by reference occurrence",
        package="markdown",
        old="3.8.2",
        new="3.9",
        source_url="https://python-markdown.github.io/changelog/",
        source_excerpt="Python-Markdown 3.9 changed footnotes to order by reference occurrence by default.",
        primary_scenario="parsing-and-ingestion",
        api_surfaces=["markdown-renderer", "library-api"],
        drift_patterns=["default-changed", "field-semantics-changed"],
        failure_modes=["silent-value-change"],
        client=HEADER
        + r'''
import re
import markdown

text = "B ref[^b] then A ref[^a]\n\n[^a]: A note\n[^b]: B note\n"
html = markdown.markdown(text, extensions=["footnotes"])
ids = re.findall(r'<li id="fn:([^"]+)"', html)
print(json.dumps({"footnote_ids": ids}, sort_keys=True))
''',
    ),
    Candidate(
        case_id="PY-STRICT-029",
        slug="python-multidict-popitem-latest-entry",
        title="multidict popitem removes the latest entry",
        package="multidict",
        old="6.2.0",
        new="6.3.0",
        source_url="https://multidict.aio-libs.org/en/stable/changes/",
        source_excerpt="multidict 6.3.0 changed MultiDict.popitem() from first entry to latest entry removal.",
        primary_scenario="state-and-lifecycle",
        api_surfaces=["mapping-api", "library-api"],
        drift_patterns=["field-semantics-changed"],
        failure_modes=["silent-value-change", "stale-state"],
        client=HEADER
        + """
from multidict import MultiDict

items = MultiDict([("a", "1"), ("b", "2"), ("a", "3")])
popped = items.popitem()
print(json.dumps({"popped": list(popped), "remaining": list(items.items())}, sort_keys=True))
""",
    ),
    Candidate(
        case_id="PY-STRICT-030",
        slug="python-sqlparse-strip-comments-whitespace",
        title="sqlparse strip_comments preserves whitespace",
        package="sqlparse",
        old="0.5.0",
        new="0.5.1",
        source_url="https://sqlparse.readthedocs.io/en/stable/changes.html#release-0-5-1-jul-15-2024",
        source_excerpt="sqlparse 0.5.1 fixed overly greedy strip_comments whitespace removal.",
        primary_scenario="parsing-and-ingestion",
        api_surfaces=["sql-formatter", "library-api"],
        drift_patterns=["parser-rule-changed", "field-semantics-changed"],
        failure_modes=["silent-value-change"],
        client=HEADER
        + r'''
import sqlparse

formatted = sqlparse.format("select 1 -- note\nfrom t", strip_comments=True)
print(json.dumps({"formatted": formatted}, sort_keys=True))
''',
    ),
    Candidate(
        case_id="PY-STRICT-031",
        slug="python-docutils-html5-footnotes-aside",
        title="Docutils HTML5 writer wraps footnotes in aside",
        package="docutils",
        old="0.18.1",
        new="0.19",
        source_url="https://docutils.sourceforge.io/RELEASE-NOTES.html#release-0-19-2022-07-05",
        source_excerpt="Docutils 0.19 changed HTML5 output for footnotes and related blocks to use semantic elements.",
        primary_scenario="parsing-and-ingestion",
        api_surfaces=["rst-renderer", "library-api"],
        drift_patterns=["field-semantics-changed", "type-or-shape-changed"],
        failure_modes=["silent-value-change"],
        client=HEADER
        + r'''
from docutils.core import publish_parts

body = publish_parts(
    "Text [1]_\n\n.. [1] note\n",
    writer_name="html5",
    settings_overrides={"report_level": 5, "halt_level": 6},
)["body"]
print(json.dumps({"has_aside": "<aside" in body, "has_dl": "<dl" in body}, sort_keys=True))
''',
    ),
    Candidate(
        case_id="PY-STRICT-032",
        slug="python-jsonpickle-make-refs-false-repeats",
        title="jsonpickle make_refs False serializes repeated objects",
        package="jsonpickle",
        old="1.4.2",
        new="1.5.0",
        source_url="https://jsonpickle.github.io/history.html#v1-5-0",
        source_excerpt="jsonpickle 1.5.0 changed make_refs=False so repeated objects are serialized instead of emitted as null.",
        primary_scenario="serialization-and-binding",
        api_surfaces=["json-serializer", "library-api"],
        drift_patterns=["field-semantics-changed"],
        failure_modes=["silent-value-change"],
        client=HEADER
        + """
import jsonpickle

shared = {"x": 1}
encoded = jsonpickle.encode([shared, shared], make_refs=False, unpicklable=False)
print(json.dumps({"encoded": encoded}, sort_keys=True))
""",
    ),
    Candidate(
        case_id="PY-STRICT-033",
        slug="python-dotenv-set-key-auto-quote",
        title="python-dotenv set_key auto quote output changes",
        package="python-dotenv",
        old="0.17.1",
        new="0.18.0",
        source_url="https://bbc2.github.io/python-dotenv/changelog/#0180-2021-06-20",
        source_excerpt="python-dotenv 0.18.0 changed set_key and dotenv set quote behavior.",
        primary_scenario="serialization-and-binding",
        api_surfaces=["environment-file-writer", "library-api"],
        drift_patterns=["default-changed", "field-semantics-changed"],
        failure_modes=["silent-value-change"],
        client=HEADER
        + """
import os
import tempfile
from dotenv import set_key

fd, path = tempfile.mkstemp()
os.close(fd)
try:
    set_key(path, "TOKEN", "abc123", quote_mode="auto")
    text = open(path, encoding="utf-8").read()
finally:
    os.remove(path)
print(json.dumps({"text": text}, sort_keys=True))
""",
    ),
    Candidate(
        case_id="PY-STRICT-034",
        slug="python-structlog-default-log-level-field",
        title="structlog default logger adds level information",
        package="structlog",
        old="20.1.0",
        new="20.2.0",
        source_url="https://www.structlog.org/en/22.1.0/changelog.html#id77",
        source_excerpt="structlog 20.2.0 changed its default configuration, including adding log level processing.",
        primary_scenario="serialization-and-binding",
        api_surfaces=["logging-api", "library-api"],
        drift_patterns=["default-changed", "field-semantics-changed"],
        failure_modes=["silent-value-change"],
        client=HEADER
        + r'''
import contextlib
import io
import structlog

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    structlog.get_logger().info("probe")
print(json.dumps({"stdout": buf.getvalue().strip()}, sort_keys=True))
''',
    ),
    Candidate(
        case_id="PY-STRICT-035",
        slug="python-hypothesis-example-db-gitignore",
        title="Hypothesis creates a gitignore in example database directories",
        package="hypothesis",
        old="6.151.14",
        new="6.152.0",
        source_url="https://hypothesis.readthedocs.io/en/latest/changelog.html",
        source_excerpt="Hypothesis 6.152.0 creates a .gitignore file in the .hypothesis directory.",
        primary_scenario="state-and-lifecycle",
        api_surfaces=["test-data-cache", "library-api"],
        drift_patterns=["default-changed", "field-semantics-changed"],
        failure_modes=["silent-side-effect-change", "stale-state"],
        timeout_s=90,
        client=HEADER
        + """
import tempfile
from pathlib import Path
from hypothesis.database import DirectoryBasedExampleDatabase

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / ".hypothesis" / "examples"
    db = DirectoryBasedExampleDatabase(path)
    db.save(b"key", b"value")
    gitignore = path.parent / ".gitignore"
    print(json.dumps({"gitignore_exists": gitignore.exists(), "gitignore_text": gitignore.read_text() if gitignore.exists() else ""}, sort_keys=True))
""",
    ),
    Candidate(
        case_id="PY-STRICT-036",
        slug="python-requests-json-utf8-response-text",
        title="requests decodes JSON response bytes as UTF-8",
        package="requests",
        old="2.25.0",
        new="2.25.1",
        source_url="https://github.com/psf/requests/blob/main/HISTORY.md",
        source_excerpt="requests 2.25.1 changed default encoding detection for application/json responses.",
        primary_scenario="parsing-and-ingestion",
        api_surfaces=["http-response-decoder", "library-api"],
        drift_patterns=["default-changed", "field-semantics-changed"],
        failure_modes=["silent-value-change", "wrong-locale"],
        client=HEADER
        + r'''
import requests

response = requests.Response()
response.status_code = 200
response.url = "https://example.test/data"
response.headers["Content-Type"] = "application/json"
response._content = '{"name":"caf\u00e9"}'.encode("utf-8")
print(json.dumps({"encoding": response.encoding, "text": response.text}, sort_keys=True))
''',
    ),
    Candidate(
        case_id="PY-STRICT-037",
        slug="python-arrow-zoneinfo-timezone-type",
        title="Arrow returns zoneinfo time zones for named zones",
        package="arrow",
        old="1.3.0",
        new="1.4.0",
        source_url="https://arrow.readthedocs.io/en/stable/releases.html",
        source_excerpt="Arrow 1.4.0 migrated timezone handling to Python zoneinfo.",
        primary_scenario="time-and-localization",
        api_surfaces=["datetime-api", "library-api"],
        drift_patterns=["field-semantics-changed", "type-or-shape-changed"],
        failure_modes=["silent-value-change", "wrong-timezone"],
        client=HEADER
        + """
import arrow

value = arrow.get(2024, 1, 1, tzinfo="Europe/Paris")
tz = value.tzinfo
print(json.dumps({"tz_class": type(tz).__name__, "tz_module": type(tz).__module__}, sort_keys=True))
""",
    ),
    Candidate(
        case_id="PY-STRICT-038",
        slug="python-emoji-unicode-15-1-face-bags",
        title="emoji recognizes Unicode 15.1 face with bags under eyes",
        package="emoji",
        old="2.13.2",
        new="2.14.0",
        source_url="https://github.com/carpedm20/emoji/blob/master/CHANGES.md",
        source_excerpt="emoji 2.14.0 updates emoji data so newer Unicode emoji are recognized by the same public API.",
        primary_scenario="validation-and-policy",
        api_surfaces=["emoji-classifier", "library-api"],
        drift_patterns=["bundled-data-changed", "validation-relaxed"],
        failure_modes=["silent-acceptance-change", "silent-value-change"],
        client=HEADER
        + r'''
import emoji

value = "\U0001FAE9"
print(json.dumps({
    "is_emoji": emoji.is_emoji(value),
    "emoji_count": emoji.emoji_count(value),
    "demojize": emoji.demojize(value),
}, sort_keys=True))
''',
    ),
    Candidate(
        case_id="PY-STRICT-039",
        slug="python-wcwidth-hangul-jamo-zero-width",
        title="wcwidth changes Hangul Jamo character widths",
        package="wcwidth",
        old="0.2.12",
        new="0.2.13",
        source_url="https://pypi.org/project/wcwidth/0.2.13/",
        source_excerpt="wcwidth 0.2.13 updates Unicode width tables used by wcwidth().",
        primary_scenario="time-and-localization",
        api_surfaces=["unicode-width", "library-api"],
        drift_patterns=["bundled-data-changed", "field-semantics-changed"],
        failure_modes=["silent-value-change"],
        client=HEADER
        + r'''
from wcwidth import wcwidth

print(json.dumps({
    "hangul_jungseong_filler": wcwidth("\u1160"),
    "hangul_jungseong_a": wcwidth("\u1161"),
}, sort_keys=True))
''',
    ),
    Candidate(
        case_id="PY-STRICT-040",
        slug="python-phonenumbers-us-645-validity",
        title="phonenumbers starts accepting US 645 numbers",
        package="phonenumbers",
        old="8.13.27",
        new="8.13.28",
        source_url="https://github.com/daviddrysdale/python-phonenumbers/blob/dev/README.md",
        source_excerpt="phonenumbers mirrors libphonenumber metadata; the version pair changes US 645 number classification.",
        primary_scenario="validation-and-policy",
        api_surfaces=["phone-number-validation", "library-api"],
        drift_patterns=["bundled-data-changed", "validation-relaxed"],
        failure_modes=["silent-acceptance-change", "silent-value-change"],
        client=HEADER
        + r'''
import phonenumbers

number = phonenumbers.parse("+16455550123", "US")
print(json.dumps({
    "valid": phonenumbers.is_valid_number(number),
    "region": phonenumbers.region_code_for_number(number),
    "type": phonenumbers.number_type(number),
}, sort_keys=True))
''',
    ),
    Candidate(
        case_id="PY-STRICT-041",
        slug="python-pytz-asia-choibalsan-2007-offset",
        title="pytz changes Asia/Choibalsan historical offset",
        package="pytz",
        old="2024.1",
        new="2024.2",
        source_url="https://data.iana.org/time-zones/tzdb-2024b/NEWS",
        source_excerpt="IANA tzdb 2024b changes historical data consumed by pytz 2024.2.",
        primary_scenario="time-and-localization",
        api_surfaces=["timezone-data", "library-api"],
        drift_patterns=["bundled-data-changed"],
        failure_modes=["wrong-timezone", "silent-value-change"],
        client=HEADER
        + """
from datetime import datetime
import pytz

zone = pytz.timezone("Asia/Choibalsan")
dt = zone.localize(datetime(2007, 1, 1, 12, 0))
print(json.dumps({"offset_seconds": int(dt.utcoffset().total_seconds()), "tzname": dt.tzname()}, sort_keys=True))
""",
    ),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append", default=[])
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--venv-root", default="D:/sdv")
    args = parser.parse_args()

    selected = [
        item
        for item in CANDIDATES
        if not args.only or item.case_id in args.only or item.slug in args.only
    ]
    python_by_key = {
        "3.10": ROOT / ".uv-python" / "cpython-3.10.20-windows-x86_64-none" / "python.exe",
        "3.9": Path.home() / "AppData" / "Roaming" / "uv" / "python" / "cpython-3.9.25-windows-x86_64-none" / "python.exe",
    }
    for version, python in python_by_key.items():
        if not python.exists():
            raise SystemExit(f"missing Python {version} executable: {python}")

    summary = {"created": [], "failed": {}, "skipped": []}
    for candidate in selected:
        print(f"== {candidate.case_id} {candidate.slug}", flush=True)
        try:
            package_dir = _run_one(candidate, python_by_key[candidate.python], Path(args.venv_root), args.force)
            summary["created"].append(str(package_dir.relative_to(ROOT)))
        except FileExistsError as exc:
            print(f"SKIP {candidate.slug}: {exc}", flush=True)
            summary["skipped"].append(candidate.slug)
        except Exception as exc:
            print(f"FAIL {candidate.slug}: {exc}", flush=True)
            summary["failed"][candidate.slug] = str(exc)
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    return 0 if not summary["failed"] else 1


def _run_one(candidate: Candidate, python: Path, venv_root: Path, force: bool) -> Path:
    if _major(candidate.old) != _major(candidate.new):
        raise RuntimeError(f"major changed: {candidate.old} -> {candidate.new}")
    _assert_not_yanked(candidate.package, candidate.old)
    _assert_not_yanked(candidate.package, candidate.new)

    package_dir = ROOT / "docs" / "case-bank" / "cases" / candidate.primary_scenario / candidate.slug
    if package_dir.exists() and not force:
        raise FileExistsError(package_dir)

    artifact_root = ROOT / "data" / "verification" / "strict_python_new" / candidate.slug
    if artifact_root.exists() and force:
        shutil.rmtree(artifact_root)
    artifact_root.mkdir(parents=True, exist_ok=True)
    client = artifact_root / "client.py"
    candidate_json = artifact_root / "candidate.json"
    client.write_text(candidate.client.strip() + "\n", encoding="utf-8")
    candidate_json.write_text(
        json.dumps(
            {
                "case_id": candidate.case_id,
                "candidate_id": candidate.slug,
                "library": candidate.package,
                "ecosystem": "python",
                "version_old": candidate.old,
                "version_new": candidate.new,
                "confidence": "high",
                "api_surface": candidate.api_surfaces,
                "source_url": candidate.source_url,
                "source_type": "release_notes",
                "retrieved_at": "2026-05-24",
                "excerpt": candidate.source_excerpt,
                "review_notes": "Strict new-candidate probe: old/new both must exit 0, emit empty stderr, and produce a stable JSON stdout difference.",
                "drift_patterns": candidate.drift_patterns,
                "failure_modes": candidate.failure_modes,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    spec = create_reproduction_spec(
        candidate_id=candidate.slug,
        library=candidate.package,
        old_version=candidate.old,
        new_version=candidate.new,
        client_file=client,
        old_python_executable=str(python),
        new_python_executable=str(python),
        extra_packages=candidate.extra_packages,
    )
    result = run_reproduction_spec(
        spec,
        artifact_root,
        timeout_s=candidate.timeout_s,
        install=True,
        venv_root=venv_root,
        build_timeout_s=candidate.build_timeout_s,
    )
    _assert_clean(result)
    return create_case_bank_package(
        CaseBankPackageRequest(
            reproduction_result=Path(result.attempt_dir) / "result.json",
            candidate=candidate_json,
            client=client,
            out_root=ROOT / "docs" / "case-bank" / "cases",
            primary_scenario=candidate.primary_scenario,
            case_id=candidate.case_id,
            slug=candidate.slug,
            title=candidate.title,
            status="verified_keep",
            source_urls=[candidate.source_url],
            source_excerpt=candidate.source_excerpt,
            retrieved_at="2026-05-24",
            ecosystem="python",
            languages=["python"],
            api_surfaces=candidate.api_surfaces,
            application_scenarios=candidate.application_scenarios or [candidate.primary_scenario],
            drift_patterns=candidate.drift_patterns,
            failure_modes=candidate.failure_modes,
            determinism="local-deterministic",
            external_dependencies="package-cache",
            review_notes="Generated after clean old/new local reproduction under strict silent-drift gates.",
            overwrite=force,
        )
    )


def _assert_clean(result) -> None:
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


def _major(version: str) -> str:
    return version.split(".", 1)[0]


_PYPI_CACHE: dict[str, dict] = {}


def _pypi_payload(package: str) -> dict:
    if package not in _PYPI_CACHE:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{package}/json", timeout=30) as response:
            _PYPI_CACHE[package] = json.loads(response.read().decode("utf-8"))
    return _PYPI_CACHE[package]


def _assert_not_yanked(package: str, version: str) -> None:
    releases = _pypi_payload(package).get("releases", {})
    files = releases.get(version)
    if not files:
        raise RuntimeError(f"{package}=={version} not found on PyPI")
    if all(file.get("yanked", False) for file in files):
        raise RuntimeError(f"{package}=={version} is yanked")


if __name__ == "__main__":
    raise SystemExit(main())
