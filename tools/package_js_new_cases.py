from __future__ import annotations

import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from probe_js_new_candidates import CANDIDATES  # noqa: E402


@dataclass(frozen=True)
class CaseSpec:
    case_id: str
    slug: str
    title: str
    primary_scenario: str
    application_scenarios: list[str]
    api_surfaces: list[str]
    drift_patterns: list[str]
    failure_modes: list[str]
    old_version: str
    new_version: str
    old_stdout: str
    new_stdout: str
    assertion_name: str
    assertion_field: str
    assertion_old: object
    assertion_new: object
    old_behavior: str
    new_behavior: str
    impact: str


CASE_SPECS = [
    CaseSpec(
        case_id="JS-11",
        slug="js-semver-coerce-include-prerelease",
        title="semver coerce preserves prerelease when requested",
        primary_scenario="validation-and-policy",
        application_scenarios=["validation-and-policy", "serialization-and-binding"],
        api_surfaces=["library-api", "version-parser"],
        drift_patterns=["field-semantics-changed", "validation-relaxed"],
        failure_modes=["silent-value-change", "silent-acceptance-change"],
        old_version="semver 7.5.4",
        new_version="semver 7.6.0",
        old_stdout='{"version":"1.2.3"}',
        new_stdout='{"version":"1.2.3-beta.4"}',
        assertion_name="coerced version includes prerelease",
        assertion_field="version",
        assertion_old="1.2.3",
        assertion_new="1.2.3-beta.4",
        old_behavior="`semver.coerce(..., { includePrerelease: true })` returns `1.2.3`.",
        new_behavior="The same call returns `1.2.3-beta.4`.",
        impact="Version filtering code can silently admit or preserve prerelease labels that were previously stripped.",
    ),
    CaseSpec(
        case_id="JS-12",
        slug="js-htmlparser2-textarea-special-tag",
        title="htmlparser2 treats textarea content as text",
        primary_scenario="parsing-and-ingestion",
        application_scenarios=["parsing-and-ingestion", "serialization-and-binding"],
        api_surfaces=["library-api", "html-parser"],
        drift_patterns=["parser-rule-changed", "type-or-shape-changed"],
        failure_modes=["wrong-type", "silent-value-change"],
        old_version="htmlparser2 9.0.0",
        new_version="htmlparser2 9.1.0",
        old_stdout='{"childType":"tag","childName":"b","childData":null}',
        new_stdout='{"childType":"text","childName":null,"childData":"<b>x</b>"}',
        assertion_name="textarea child node type changes",
        assertion_field="childType",
        assertion_old="tag",
        assertion_new="text",
        old_behavior="Parsing `<textarea><b>x</b></textarea>` creates a nested `b` tag child.",
        new_behavior="The same input keeps `<b>x</b>` as textarea text.",
        impact="HTML sanitizers or content extractors can silently change tree shape for textarea payloads.",
    ),
    CaseSpec(
        case_id="JS-13",
        slug="js-ajv-jtd-optional-leading-comma",
        title="AJV JTD serializer removes leading comma for optional-only objects",
        primary_scenario="serialization-and-binding",
        application_scenarios=["serialization-and-binding"],
        api_surfaces=["library-api", "json-serializer"],
        drift_patterns=["field-semantics-changed"],
        failure_modes=["silent-value-change"],
        old_version="ajv 8.11.2",
        new_version="ajv 8.12.0",
        old_stdout='{"serialized":"{,\\"b\\":1}"}',
        new_stdout='{"serialized":"{\\"b\\":1}"}',
        assertion_name="serialized object no longer has leading comma",
        assertion_field="serialized",
        assertion_old='{,"b":1}',
        assertion_new='{"b":1}',
        old_behavior="A JTD serializer for an object with only optional properties emits `{,\"b\":1}` for `{ b: 1 }`.",
        new_behavior="The same serializer emits valid JSON `{\"b\":1}`.",
        impact="Generated JSON payloads can silently become parseable and change downstream acceptance behavior.",
    ),
    CaseSpec(
        case_id="JS-14",
        slug="js-query-string-encoded-separator-array",
        title="query-string stops splitting encoded separator values",
        primary_scenario="parsing-and-ingestion",
        application_scenarios=["parsing-and-ingestion", "routing-and-identity"],
        api_surfaces=["library-api", "query-parser"],
        drift_patterns=["parser-rule-changed", "type-or-shape-changed"],
        failure_modes=["wrong-type", "silent-value-change"],
        old_version="query-string 9.2.2",
        new_version="query-string 9.3.0",
        old_stdout='{"ids":["1","2"],"isArray":true}',
        new_stdout='{"ids":"1|2","isArray":false}',
        assertion_name="encoded separator remains scalar",
        assertion_field="isArray",
        assertion_old=True,
        assertion_new=False,
        old_behavior="Parsing `ids=1%7C2` with separator mode returns `ids` as `['1', '2']`.",
        new_behavior="The same parse returns the scalar string `1|2`.",
        impact="Request handlers can silently stop treating encoded separator text as multiple selected IDs.",
    ),
    CaseSpec(
        case_id="JS-15",
        slug="js-validator-leading-zero-port",
        title="validator rejects ports with leading zeros",
        primary_scenario="validation-and-policy",
        application_scenarios=["validation-and-policy", "routing-and-identity"],
        api_surfaces=["library-api", "string-validator"],
        drift_patterns=["validation-strictness-increased", "field-semantics-changed"],
        failure_modes=["silent-rejection-change", "silent-value-change"],
        old_version="validator 13.11.0",
        new_version="validator 13.12.0",
        old_stdout='{"port01":true,"port00080":true,"port80":true}',
        new_stdout='{"port01":false,"port00080":false,"port80":true}',
        assertion_name="leading-zero port is rejected",
        assertion_field="port01",
        assertion_old=True,
        assertion_new=False,
        old_behavior="`validator.isPort('01')` returns `true`.",
        new_behavior="The same call returns `false`.",
        impact="Configuration or URL validators can silently reject port strings they previously accepted.",
    ),
    CaseSpec(
        case_id="JS-16",
        slug="js-whatwg-url-caret-percent-encoding",
        title="whatwg-url percent-encodes caret in URL paths",
        primary_scenario="routing-and-identity",
        application_scenarios=["routing-and-identity", "serialization-and-binding"],
        api_surfaces=["library-api", "url-parser"],
        drift_patterns=["parser-rule-changed", "field-semantics-changed"],
        failure_modes=["wrong-route", "silent-value-change"],
        old_version="whatwg-url 14.1.1",
        new_version="whatwg-url 14.2.0",
        old_stdout='{"href":"https://example.test/a^b?x=1^2","pathname":"/a^b","search":"?x=1^2"}',
        new_stdout='{"href":"https://example.test/a%5Eb?x=1^2","pathname":"/a%5Eb","search":"?x=1^2"}',
        assertion_name="path caret is encoded",
        assertion_field="pathname",
        assertion_old="/a^b",
        assertion_new="/a%5Eb",
        old_behavior="Constructing a URL with path `a^b` preserves the caret in `pathname`.",
        new_behavior="The same constructor percent-encodes the path caret.",
        impact="Routing keys, cache keys, or signature bases derived from URL strings can silently change.",
    ),
    CaseSpec(
        case_id="JS-17",
        slug="js-is-core-module-node-test-registry",
        title="is-core-module recognizes node:test for Node 18",
        primary_scenario="runtime-semantics",
        application_scenarios=["runtime-semantics", "validation-and-policy"],
        api_surfaces=["library-api", "runtime-module-registry"],
        drift_patterns=["bundled-data-changed", "validation-relaxed"],
        failure_modes=["silent-acceptance-change", "silent-value-change"],
        old_version="is-core-module 2.8.1",
        new_version="is-core-module 2.9.0",
        old_stdout='{"nodeTest18":false,"nodeTest16":false}',
        new_stdout='{"nodeTest18":true,"nodeTest16":false}',
        assertion_name="node:test is core in Node 18",
        assertion_field="nodeTest18",
        assertion_old=False,
        assertion_new=True,
        old_behavior="`isCore('node:test', '18.0.0')` returns `false`.",
        new_behavior="The same call returns `true`.",
        impact="Bundler or resolver policy can silently stop treating `node:test` as an external dependency.",
    ),
    CaseSpec(
        case_id="JS-18",
        slug="js-cookie-partitioned-serialize-option",
        title="cookie serializes the Partitioned attribute",
        primary_scenario="serialization-and-binding",
        application_scenarios=["serialization-and-binding", "routing-and-identity"],
        api_surfaces=["library-api", "cookie-serializer"],
        drift_patterns=["field-semantics-changed", "validation-relaxed"],
        failure_modes=["silent-value-change", "silent-acceptance-change"],
        old_version="cookie 0.5.0",
        new_version="cookie 0.6.0",
        old_stdout='{"text":"sid=abc; Secure; SameSite=None","hasPartitioned":false}',
        new_stdout='{"text":"sid=abc; Secure; Partitioned; SameSite=None","hasPartitioned":true}',
        assertion_name="partitioned attribute is emitted",
        assertion_field="hasPartitioned",
        assertion_old=False,
        assertion_new=True,
        old_behavior="`cookie.serialize(..., { partitioned: true })` omits the `Partitioned` attribute.",
        new_behavior="The same call emits `Partitioned` in the Set-Cookie string.",
        impact="Cookie writers can silently start sending CHIPS/partitioned-cookie attributes to clients.",
    ),
    CaseSpec(
        case_id="JS-19",
        slug="js-mime-db-parquet-media-type",
        title="mime-db adds the Apache Parquet media type",
        primary_scenario="parsing-and-ingestion",
        application_scenarios=["parsing-and-ingestion", "validation-and-policy"],
        api_surfaces=["library-api", "mime-registry"],
        drift_patterns=["bundled-data-changed", "validation-relaxed"],
        failure_modes=["silent-acceptance-change", "silent-value-change"],
        old_version="mime-db 1.52.0",
        new_version="mime-db 1.53.0",
        old_stdout='{"exists":false,"extensions":null}',
        new_stdout='{"exists":true,"extensions":null}',
        assertion_name="parquet media type exists",
        assertion_field="exists",
        assertion_old=False,
        assertion_new=True,
        old_behavior="The MIME registry has no `application/vnd.apache.parquet` entry.",
        new_behavior="The same registry lookup returns an entry for `application/vnd.apache.parquet`.",
        impact="Upload filters, content classifiers, or serializers can silently start recognizing Parquet payloads.",
    ),
    CaseSpec(
        case_id="JS-20",
        slug="js-spdx-license-ids-pkgconf-added",
        title="spdx-license-ids adds pkgconf",
        primary_scenario="validation-and-policy",
        application_scenarios=["validation-and-policy"],
        api_surfaces=["library-api", "license-registry"],
        drift_patterns=["bundled-data-changed", "validation-relaxed"],
        failure_modes=["silent-acceptance-change", "silent-value-change"],
        old_version="spdx-license-ids 3.0.17",
        new_version="spdx-license-ids 3.0.18",
        old_stdout='{"hasPkgconf":false,"count":606}',
        new_stdout='{"hasPkgconf":true,"count":628}',
        assertion_name="pkgconf license id is present",
        assertion_field="hasPkgconf",
        assertion_old=False,
        assertion_new=True,
        old_behavior="The exported SPDX identifier list does not include `pkgconf`.",
        new_behavior="The same list includes `pkgconf`.",
        impact="License allow/deny checks can silently classify package metadata differently after a registry update.",
    ),
    CaseSpec(
        case_id="JS-21",
        slug="js-set-cookie-parser-partitioned-attribute",
        title="set-cookie-parser recognizes Partitioned cookies",
        primary_scenario="parsing-and-ingestion",
        application_scenarios=["parsing-and-ingestion", "routing-and-identity"],
        api_surfaces=["library-api", "cookie-parser"],
        drift_patterns=["parser-rule-changed", "validation-relaxed"],
        failure_modes=["silent-acceptance-change", "silent-value-change"],
        old_version="set-cookie-parser 2.6.0",
        new_version="set-cookie-parser 2.7.0",
        old_stdout='{"partitioned":false,"secure":true,"sameSite":"None"}',
        new_stdout='{"partitioned":true,"secure":true,"sameSite":"None"}',
        assertion_name="partitioned cookie attribute is parsed",
        assertion_field="partitioned",
        assertion_old=False,
        assertion_new=True,
        old_behavior="Parsing `Partitioned` leaves no positive `partitioned` flag.",
        new_behavior="The same Set-Cookie header parses with `partitioned: true`.",
        impact="Reverse proxies or session middleware can silently start treating the same cookie as partitioned.",
    ),
    CaseSpec(
        case_id="JS-22",
        slug="js-builtin-modules-node-ffi-added",
        title="builtin-modules adds node:ffi",
        primary_scenario="runtime-semantics",
        application_scenarios=["runtime-semantics", "validation-and-policy"],
        api_surfaces=["library-api", "runtime-module-registry"],
        drift_patterns=["bundled-data-changed", "validation-relaxed"],
        failure_modes=["silent-acceptance-change", "silent-value-change"],
        old_version="builtin-modules 5.1.0",
        new_version="builtin-modules 5.2.0",
        old_stdout='{"hasNodeFfi":false,"count":113}',
        new_stdout='{"hasNodeFfi":true,"count":114}',
        assertion_name="node:ffi is listed as built in",
        assertion_field="hasNodeFfi",
        assertion_old=False,
        assertion_new=True,
        old_behavior="The exported built-in module list does not include `node:ffi`.",
        new_behavior="The same list includes `node:ffi`.",
        impact="Bundlers and dependency analyzers can silently stop treating `node:ffi` as an external package name.",
    ),
]


def main() -> int:
    by_slug = {candidate.slug: candidate for candidate in CANDIDATES}
    for spec in CASE_SPECS:
        candidate = by_slug[spec.slug]
        package_dir = ROOT / "docs" / "case-bank" / "cases" / spec.primary_scenario / spec.slug
        if package_dir.exists():
            shutil.rmtree(package_dir)
        (package_dir / "client").mkdir(parents=True)
        (package_dir / "hidden").mkdir()
        _write_package(spec, candidate, package_dir)
        print(package_dir.relative_to(ROOT))
    return 0


def _write_package(spec: CaseSpec, candidate, package_dir: Path) -> None:
    metadata = {
        "case_id": spec.case_id,
        "slug": spec.slug,
        "title": spec.title,
        "status": "verified_keep",
        "primary_scenario": spec.primary_scenario,
        "application_scenarios": spec.application_scenarios,
        "ecosystems": ["js"],
        "languages": ["javascript"],
        "api_surfaces": spec.api_surfaces,
        "drift_patterns": spec.drift_patterns,
        "failure_modes": spec.failure_modes,
        "determinism": "local-deterministic",
        "external_dependencies": "package-cache",
        "old_version": spec.old_version,
        "new_version": spec.new_version,
        "source_urls": [candidate.source],
        "provenance": {
            "reproduction_result": f"data/verification/js_new_probe/{spec.slug}",
            "verified_at": "2026-05-24",
            "old_stdout": spec.old_stdout,
            "new_stdout": spec.new_stdout,
            "old_exit": 0,
            "new_exit": 0,
            "old_stderr": "",
            "new_stderr": "",
        },
    }
    (package_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    (package_dir / "case.md").write_text(_case_markdown(spec, candidate), encoding="utf-8")
    (package_dir / "evidence.md").write_text(_evidence_markdown(spec, candidate), encoding="utf-8")
    (package_dir / "env.md").write_text(_env_markdown(spec, candidate), encoding="utf-8")
    (package_dir / "hidden" / "oracle.md").write_text(_oracle_markdown(spec), encoding="utf-8")
    (package_dir / "hidden" / "expected.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "case_id": spec.case_id,
                "assertions": [
                    {
                        "name": spec.assertion_name,
                        "field": spec.assertion_field,
                        "old": spec.assertion_old,
                        "new": spec.assertion_new,
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    package_json: dict[str, object] = {
        "private": True,
        "scripts": {"probe": "node probe.mjs" if candidate.module_type == "module" else "node probe.js"},
        "dependencies": {candidate.package: candidate.new},
        "silentDrift": {"package": candidate.package, "old": candidate.old, "new": candidate.new},
    }
    if candidate.module_type == "module":
        package_json["type"] = "module"
    (package_dir / "client" / "package.json").write_text(json.dumps(package_json, indent=2) + "\n", encoding="utf-8")
    probe_name = "probe.mjs" if candidate.module_type == "module" else "probe.js"
    (package_dir / "client" / probe_name).write_text(candidate.client, encoding="utf-8")


def _case_markdown(spec: CaseSpec, candidate) -> str:
    return "\n".join(
        [
            f"# {spec.case_id}: {spec.title}",
            "",
            "## API Or Behavior Under Test",
            "",
            f"`{candidate.package}` public API in the copied client probe.",
            "",
            "## Version Boundary",
            "",
            f"{spec.old_version} -> {spec.new_version}",
            "",
            "## Old Behavior",
            "",
            spec.old_behavior,
            "",
            "## New Behavior",
            "",
            spec.new_behavior,
            "",
            "## Why The Drift Is Silent",
            "",
            "The same Node client exits 0 in both versions with empty stderr and stable JSON stdout; only the returned semantics change.",
            "",
            "## Realistic Impact Scenario",
            "",
            spec.impact,
            "",
        ]
    )


def _evidence_markdown(spec: CaseSpec, candidate) -> str:
    return "\n".join(
        [
            f"# Evidence For {spec.case_id}",
            "",
            "## Source URLs",
            "",
            f"- {candidate.source}",
            "",
            "## Local Reproduction",
            "",
            f"- Old: `{spec.old_version}`",
            f"- New: `{spec.new_version}`",
            f"- Old stdout: `{spec.old_stdout}`",
            f"- New stdout: `{spec.new_stdout}`",
            "- Old/new exit code: 0",
            "- Old/new stderr: empty",
            f"- Verification path: `data/verification/js_new_probe/{spec.slug}`",
            "",
        ]
    )


def _env_markdown(spec: CaseSpec, candidate) -> str:
    return "\n".join(
        [
            f"# Environment For {spec.case_id}",
            "",
            "- Runtime: Node.js with npm package installation enabled.",
            f"- Package versions: `{spec.old_version}` and `{spec.new_version}`.",
            "- Version switching: edit `client/package.json` to pin the target package version, then run `npm install`.",
            "- Adapter/API surface: library-api.",
            "- Probe shape: run the copied Node probe and parse one JSON object from stdout.",
            "- Command shape: `npm install --silent --no-audit --fund=false`, then `npm run probe --silent`.",
            "",
        ]
    )


def _oracle_markdown(spec: CaseSpec) -> str:
    return "\n".join(
        [
            f"# Oracle For {spec.case_id}",
            "",
            f"Run the probe against {spec.old_version} and {spec.new_version}.",
            "",
            f"The old run must produce `{spec.old_stdout}` with exit code 0 and empty stderr.",
            "",
            f"The new run must produce `{spec.new_stdout}` with exit code 0 and empty stderr.",
            "",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
