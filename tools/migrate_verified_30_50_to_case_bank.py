"""Materialize verified old-pipeline 30/50 cases as case-bank packages.

The source set is the verified portion of:
- data/verification/sequential_30
- data/verification/reverse_50
"""
from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = ROOT / "docs" / "case-bank" / "cases"
VERIFIED_AT = "2026-05-21"


def clean(value: str) -> str:
    return textwrap.dedent(value).strip() + "\n"


def package_json(name: str, deps: dict[str, str] | None = None) -> str:
    data: dict[str, Any] = {
        "name": name,
        "version": "1.0.0",
        "private": True,
        "scripts": {"probe": "node probe.js"},
    }
    if deps:
        data["dependencies"] = deps
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def dotnet_project(package: str) -> str:
    return clean(
        f"""
        <Project Sdk="Microsoft.NET.Sdk">
          <PropertyGroup>
            <OutputType>Exe</OutputType>
            <TargetFramework>net7.0</TargetFramework>
            <ImplicitUsings>enable</ImplicitUsings>
            <Nullable>enable</Nullable>
          </PropertyGroup>
          <ItemGroup>
            <PackageReference Include="{package}" Version="*" />
          </ItemGroup>
        </Project>
        """
    )


def simple_pom(group_id: str, artifact_id: str, deps: str) -> str:
    return clean(
        f"""
        <project xmlns="http://maven.apache.org/POM/4.0.0"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
          <modelVersion>4.0.0</modelVersion>
          <groupId>{group_id}</groupId>
          <artifactId>{artifact_id}</artifactId>
          <version>1.0.0</version>
          <properties>
            <maven.compiler.source>17</maven.compiler.source>
            <maven.compiler.target>17</maven.compiler.target>
          </properties>
          <dependencies>
        {textwrap.indent(textwrap.dedent(deps).strip(), "    ")}
          </dependencies>
        </project>
        """
    )


def case(
    *,
    case_id: str,
    slug: str,
    title: str,
    primary: str,
    ecosystems: list[str],
    languages: list[str],
    api_surfaces: list[str],
    drift_patterns: list[str],
    failure_modes: list[str],
    old_version: str,
    new_version: str,
    source_urls: list[str],
    reproduction_result: str,
    behavior_under_test: str,
    old_behavior: str,
    new_behavior: str,
    why_silent: str,
    impact: str,
    source_notes: str,
    env_notes: list[str],
    assertions: list[dict[str, Any]],
    client_files: dict[str, str],
    application_scenarios: list[str] | None = None,
    determinism: str = "local-deterministic",
    external_dependencies: str = "package-cache",
) -> dict[str, Any]:
    scenarios = application_scenarios or [primary]
    if primary not in scenarios:
        scenarios = [primary, *scenarios]
    return {
        "case_id": case_id,
        "slug": slug,
        "title": title,
        "status": "verified_keep",
        "primary_scenario": primary,
        "application_scenarios": scenarios,
        "ecosystems": ecosystems,
        "languages": languages,
        "api_surfaces": api_surfaces,
        "drift_patterns": drift_patterns,
        "failure_modes": failure_modes,
        "determinism": determinism,
        "external_dependencies": external_dependencies,
        "old_version": old_version,
        "new_version": new_version,
        "source_urls": source_urls,
        "provenance": {
            "reproduction_result": reproduction_result,
            "verified_at": VERIFIED_AT,
        },
        "_case": {
            "behavior_under_test": behavior_under_test,
            "old_behavior": old_behavior,
            "new_behavior": new_behavior,
            "why_silent": why_silent,
            "impact": impact,
        },
        "_evidence": {"source_notes": source_notes},
        "_env": env_notes,
        "_expected": {"schema_version": 1, "case_id": case_id, "assertions": assertions},
        "_client_files": client_files,
    }


COMMON_GITIGNORE = "__pycache__/\n*.pyc\n.venv/\nnode_modules/\nvendor/\n.bundle/\nbin/\nobj/\ntarget/\n*.class\n*.sqlite\n"


CASES: list[dict[str, Any]] = [
    case(
        case_id="DOTNET-05",
        slug="dotnet-configurationbinder-dictionary-append",
        title="ConfigurationBinder appends dictionary collection values",
        primary="serialization-and-binding",
        application_scenarios=["serialization-and-binding", "state-and-lifecycle"],
        ecosystems=["dotnet"],
        languages=["csharp"],
        api_surfaces=["configuration-binder", "library-api"],
        drift_patterns=["default-changed", "old-state-overwrite"],
        failure_modes=["silent-value-change", "stale-state"],
        old_version="Microsoft.Extensions.Configuration.Binder 6.x",
        new_version="Microsoft.Extensions.Configuration.Binder 7.x",
        source_urls=[
            "https://learn.microsoft.com/en-us/dotnet/core/compatibility/extensions/7.0/config-bind-dictionary"
        ],
        reproduction_result="data/verification/sequential_30/DOTNET-05",
        behavior_under_test="Binding configuration into an existing dictionary whose value is a collection.",
        old_behavior="The binder replaces the existing collection with the configured value.",
        new_behavior="The binder extends the existing collection and preserves the prior value.",
        why_silent="The bind call succeeds in both versions and returns the same object type.",
        impact="A service can keep stale configured values after an upgrade, changing effective routing, allowlists, or feature flags.",
        source_notes="The .NET 7 compatibility note documents dictionary values being extended instead of replaced.",
        env_notes=[
            "Runtime: .NET SDK with Microsoft.Extensions.Configuration.Binder installed.",
            "Version switching: restore with Binder 6.x for old and 7.x for new.",
            "Probe shape: run Program.cs and compare the pipe-delimited value list from stdout.",
        ],
        assertions=[
            {
                "name": "dictionary collection binding preserves old item",
                "field": "values.Key",
                "old": ["NewValue"],
                "new": ["InitialValue", "NewValue"],
            }
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "probe.csproj": dotnet_project("Microsoft.Extensions.Configuration.Binder"),
            "Program.cs": clean(
                """
                using Microsoft.Extensions.Configuration;

                var seed = new Dictionary<string, string?>
                {
                    ["Key:0"] = "NewValue"
                };
                var config = new ConfigurationBuilder().AddInMemoryCollection(seed).Build();
                var target = new Dictionary<string, string[]>
                {
                    ["Key"] = new[] { "InitialValue" }
                };

                config.Bind(target);
                Console.WriteLine(string.Join("|", target["Key"]));
                """
            ),
        },
    ),
    case(
        case_id="DOTNET-09",
        slug="dotnet-csvhelper-culture-delimiter",
        title="CsvHelper infers culture delimiter from CultureInfo",
        primary="parsing-and-ingestion",
        ecosystems=["dotnet"],
        languages=["csharp"],
        api_surfaces=["library-api", "csv-parser"],
        drift_patterns=["default-changed", "parser-rule-changed"],
        failure_modes=["silent-value-change"],
        old_version="CsvHelper 9.2.3",
        new_version="CsvHelper 10.0.0",
        source_urls=["https://joshclose.github.io/CsvHelper/change-log"],
        reproduction_result="data/verification/sequential_30/DOTNET-09",
        behavior_under_test="CsvReader delimiter selection when the configuration is created from a semicolon culture.",
        old_behavior="The input line is read as one field, keeping A;B together.",
        new_behavior="The same line is split into two fields, A and B.",
        why_silent="Parsing completes successfully and downstream code only sees a different row shape.",
        impact="CSV imports can silently shift columns when a deployment changes CsvHelper versions.",
        source_notes="CsvHelper 10 changed delimiter behavior around culture-aware configuration.",
        env_notes=[
            "Runtime: .NET SDK with CsvHelper installed.",
            "Version switching: restore with CsvHelper 9.2.3 for old and 10.0.0 for new.",
            "Probe shape: run Program.cs and compare field count plus joined fields.",
        ],
        assertions=[
            {"name": "field count changes", "field": "field_count", "old": 1, "new": 2},
            {"name": "parsed fields change", "field": "fields", "old": ["A;B"], "new": ["A", "B"]},
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "probe.csproj": dotnet_project("CsvHelper"),
            "Program.cs": clean(
                """
                using System.Globalization;
                using CsvHelper;
                using CsvHelper.Configuration;

                using var reader = new StringReader("A;B\\n");
                using var csv = new CsvReader(reader, new CsvConfiguration(new CultureInfo("de-DE"))
                {
                    HasHeaderRecord = false
                });
                csv.Read();
                var fields = csv.Context.Parser.Record ?? Array.Empty<string>();
                Console.WriteLine(fields.Length);
                Console.WriteLine(string.Join("|", fields));
                """
            ),
        },
    ),
    case(
        case_id="GO-001",
        slug="go-json-omitzero",
        title="encoding/json omitzero starts omitting zero fields",
        primary="serialization-and-binding",
        ecosystems=["go"],
        languages=["go"],
        api_surfaces=["standard-library", "json-encoder"],
        drift_patterns=["field-removed-or-masked", "type-or-shape-changed"],
        failure_modes=["missing-field", "silent-value-change"],
        old_version="Go 1.23.12",
        new_version="Go 1.26.3",
        source_urls=["https://go.dev/doc/go1.24"],
        reproduction_result="data/verification/sequential_30/GO-001",
        behavior_under_test="encoding/json handling of the omitzero struct tag option.",
        old_behavior="The unknown tag option is ignored and count:0 is emitted.",
        new_behavior="The tag is recognized and the zero-valued field is omitted.",
        why_silent="json.Marshal succeeds in both versions and returns valid JSON.",
        impact="Wire payloads can stop carrying zero values that older consumers used as explicit signals.",
        source_notes="The Go 1.24 release notes introduce the omitzero tag option for encoding/json.",
        env_notes=[
            "Runtime: Go toolchain pair.",
            "Version switching: run the same main.go with Go 1.23.x and Go 1.24+.",
            "Probe shape: go run . and parse one JSON object from stdout.",
        ],
        determinism="runtime-pair",
        external_dependencies="runtime-pair",
        assertions=[
            {"name": "zero field omission changes", "field": "json", "old": {"count": 0}, "new": {}}
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "go.mod": "module go001\n\ngo 1.23\n",
            "main.go": clean(
                """
                package main

                import (
                    "encoding/json"
                    "fmt"
                )

                type Payload struct {
                    Count int `json:"count,omitzero"`
                }

                func main() {
                    b, err := json.Marshal(Payload{})
                    if err != nil {
                        panic(err)
                    }
                    fmt.Println(string(b))
                }
                """
            ),
        },
    ),
    case(
        case_id="GO-003",
        slug="go-servemux-method-brace-pattern",
        title="ServeMux treats method and brace patterns as structured routes",
        primary="routing-and-identity",
        ecosystems=["go"],
        languages=["go"],
        api_surfaces=["standard-library", "http-router"],
        drift_patterns=["parser-rule-changed", "default-changed"],
        failure_modes=["wrong-route", "silent-value-change"],
        old_version="Go 1.21.x",
        new_version="Go 1.22+",
        source_urls=["https://go.dev/doc/go1.22"],
        reproduction_result="data/verification/sequential_30/GO-003",
        behavior_under_test="net/http ServeMux matching for a pattern containing an HTTP method and a path variable.",
        old_behavior="The registered pattern is treated literally and the request falls through with an empty matched pattern.",
        new_behavior="The pattern matches GET /posts/123 and returns GET /posts/{id}.",
        why_silent="The handler lookup returns a handler in both versions, but route identity changes.",
        impact="Metrics, auth, or request handling keyed by ServeMux pattern can silently attach to a different route.",
        source_notes="The Go 1.22 release notes document enhanced ServeMux pattern syntax.",
        env_notes=[
            "Runtime: Go toolchain pair.",
            "Version switching: run the same main.go with Go 1.21.x and Go 1.22+.",
            "Probe shape: go run . and compare the printed matched pattern.",
        ],
        determinism="runtime-pair",
        external_dependencies="runtime-pair",
        assertions=[
            {"name": "matched pattern changes", "field": "pattern", "old": "", "new": "GET /posts/{id}"}
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "go.mod": "module go003\n\ngo 1.21\n",
            "main.go": clean(
                """
                package main

                import (
                    "fmt"
                    "net/http"
                )

                func main() {
                    mux := http.NewServeMux()
                    mux.HandleFunc("GET /posts/{id}", func(w http.ResponseWriter, r *http.Request) {})
                    req, _ := http.NewRequest("GET", "/posts/123", nil)
                    match, pattern := mux.Handler(req)
                    fmt.Printf("pattern=%q handler=%T\\n", pattern, match)
                }
                """
            ),
        },
    ),
    case(
        case_id="GO-006",
        slug="go-test-json-build-output-events",
        title="go test -json emits structured build-output events",
        primary="observability-and-logging",
        ecosystems=["go"],
        languages=["go"],
        api_surfaces=["cli-output", "test-runner"],
        drift_patterns=["type-or-shape-changed", "out-of-order-event"],
        failure_modes=["silent-value-change"],
        old_version="Go 1.23.12",
        new_version="Go 1.26.3",
        source_urls=["https://go.dev/doc/go1.24"],
        reproduction_result="data/verification/sequential_30/GO-006",
        behavior_under_test="JSON event stream produced by go test -json when the package fails to build.",
        old_behavior="Compiler diagnostics are mixed with the JSON stream as unstructured text.",
        new_behavior="The build diagnostics appear as JSON events with Action=build-output and Action=build-fail.",
        why_silent="The command still fails, but log parsers receive a different event shape.",
        impact="CI parsers can silently drop or double-count build diagnostics after a Go toolchain upgrade.",
        source_notes="The Go 1.24 release notes document additional build-output events in test JSON output.",
        env_notes=[
            "Runtime: Go toolchain pair.",
            "Version switching: run go test -json ./... with Go 1.23.x and Go 1.24+.",
            "Probe shape: inspect stdout/stderr and count JSON events whose Action starts with build.",
        ],
        determinism="runtime-pair",
        external_dependencies="runtime-pair",
        assertions=[
            {"name": "build output becomes structured", "field": "has_build_output_event", "old": False, "new": True},
            {"name": "failed build id appears", "field": "failed_build", "old": "<missing>", "new": "go006"},
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "go.mod": "module go006\n\ngo 1.23\n",
            "broken.go": clean(
                """
                package go006

                func Broken() int {
                    return missingSymbol
                }
                """
            ),
        },
    ),
    case(
        case_id="GO-007",
        slug="go-yaml-v2-v3-boolean-strings",
        title="go-yaml v3 stops treating YAML 1.1 booleans as bools",
        primary="parsing-and-ingestion",
        ecosystems=["go"],
        languages=["go"],
        api_surfaces=["library-api", "yaml-parser"],
        drift_patterns=["parser-rule-changed", "type-or-shape-changed"],
        failure_modes=["wrong-type", "silent-value-change"],
        old_version="gopkg.in/yaml.v2",
        new_version="gopkg.in/yaml.v3",
        source_urls=["https://github.com/go-yaml/yaml/tree/v3"],
        reproduction_result="data/verification/sequential_30/GO-007",
        behavior_under_test="Decoding scalar values on and no into map values.",
        old_behavior="YAML 1.1 boolean-like strings decode as bool true and bool false.",
        new_behavior="The same scalars decode as strings.",
        why_silent="Unmarshal succeeds and no schema error is raised.",
        impact="Feature flags or config keys can silently change type when moving from yaml.v2 to yaml.v3.",
        source_notes="The yaml.v3 documentation describes YAML 1.2 oriented scalar behavior.",
        env_notes=[
            "Runtime: Go with gopkg.in/yaml.v2 or gopkg.in/yaml.v3 available.",
            "Version switching: change the import path in main.go or use the v2/v3 variants noted in comments.",
            "Probe shape: go run . and compare reflected value types.",
        ],
        assertions=[
            {"name": "on scalar type changes", "field": "flag.type", "old": "bool", "new": "string"},
            {"name": "no scalar type changes", "field": "nope.type", "old": "bool", "new": "string"},
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "go.mod": "module go007\n\ngo 1.23\n\nrequire gopkg.in/yaml.v3 v3.0.1\n",
            "main.go": clean(
                """
                package main

                import (
                    "fmt"

                    yaml "gopkg.in/yaml.v3"
                )

                func main() {
                    var out map[string]any
                    if err := yaml.Unmarshal([]byte("flag: on\\nnope: no\\n"), &out); err != nil {
                        panic(err)
                    }
                    fmt.Printf("flag=%T:%v nope=%T:%v\\n", out["flag"], out["flag"], out["nope"], out["nope"])
                }
                """
            ),
        },
    ),
    case(
        case_id="JS-01",
        slug="js-node-full-icu-locale-month",
        title="Node.js full ICU changes locale month formatting",
        primary="time-and-localization",
        ecosystems=["js"],
        languages=["javascript"],
        api_surfaces=["runtime-api", "intl"],
        drift_patterns=["runtime-locale-changed", "bundled-data-changed"],
        failure_modes=["wrong-locale", "silent-value-change"],
        old_version="Node.js 12.22.12 small-ICU",
        new_version="Node.js 13.14.0 full-ICU",
        source_urls=["https://nodejs.org/en/blog/release/v13.0.0"],
        reproduction_result="data/verification/sequential_30/JS-01",
        behavior_under_test="Intl.DateTimeFormat month formatting for Spanish.",
        old_behavior="The runtime lacks the locale data and returns M01.",
        new_behavior="The same API returns the Spanish month name enero.",
        why_silent="The formatter is constructed successfully in both runtimes.",
        impact="User-visible invoices, reports, or cache keys can change locale text without application code changes.",
        source_notes="The Node.js 13 release notes document full ICU data enabled by default.",
        env_notes=[
            "Runtime: Node.js pair with old small-ICU and new full-ICU builds.",
            "Version switching: run node client/probe.js under both runtimes.",
            "Probe shape: parse one JSON object from stdout.",
        ],
        determinism="runtime-pair",
        external_dependencies="runtime-pair",
        assertions=[
            {"name": "Spanish month changes", "field": "month", "old": "M01", "new": "enero"},
            {"name": "Spanish locale support changes", "field": "supported.es", "old": False, "new": True},
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "package.json": package_json("js-node-full-icu-locale-month"),
            "probe.js": clean(
                """
                const date = new Date(Date.UTC(2020, 0, 1));
                const month = new Intl.DateTimeFormat("es", { month: "long", timeZone: "UTC" }).format(date);
                const supported = Intl.DateTimeFormat.supportedLocalesOf(["es", "fr", "zh-CN", "ar", "hi"]);
                console.log(JSON.stringify({
                  node: process.version,
                  supported,
                  month,
                  supported_es: supported.includes("es")
                }));
                """
            ),
        },
    ),
    case(
        case_id="JS-02",
        slug="js-npm-lockfile-version",
        title="npm creates lockfileVersion 2 instead of version 1",
        primary="serialization-and-binding",
        ecosystems=["js"],
        languages=["javascript"],
        api_surfaces=["package-manager", "lockfile"],
        drift_patterns=["type-or-shape-changed", "default-changed"],
        failure_modes=["silent-value-change"],
        old_version="npm 6.x",
        new_version="npm 7.x",
        source_urls=[
            "https://blog.npmjs.org/post/626173315965468672/npm-v7-series-beta-release-and-semver-major.html"
        ],
        reproduction_result="data/verification/sequential_30/JS-02",
        behavior_under_test="package-lock.json format generated for the same package root.",
        old_behavior="npm writes lockfileVersion 1.",
        new_behavior="npm writes lockfileVersion 2.",
        why_silent="npm install succeeds in both versions and the dependency tree is still installable.",
        impact="Tooling that parses lockfiles can silently read a different schema after a package-manager upgrade.",
        source_notes="The npm v7 beta post calls out the semver-major lockfile changes.",
        env_notes=[
            "Runtime: Node.js with npm 6.x and npm 7.x available.",
            "Version switching: remove package-lock.json, run npm install --package-lock-only, then run node probe.js.",
            "Probe shape: parse package-lock.json and report lockfileVersion.",
        ],
        determinism="runtime-pair",
        external_dependencies="runtime-pair",
        assertions=[
            {"name": "lockfile format version changes", "field": "lockfileVersion", "old": 1, "new": 2}
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "package.json": package_json("js-npm-lockfile-version", {"left-pad": "1.3.0"}),
            "probe.js": clean(
                """
                const fs = require("fs");
                const lock = JSON.parse(fs.readFileSync("package-lock.json", "utf8"));
                console.log(JSON.stringify({ lockfileVersion: lock.lockfileVersion }));
                """
            ),
        },
    ),
    case(
        case_id="JS-03",
        slug="js-prettier-trailing-comma-default",
        title="Prettier 3 adds trailing commas by default",
        primary="serialization-and-binding",
        ecosystems=["js"],
        languages=["javascript"],
        api_surfaces=["formatter", "library-api"],
        drift_patterns=["default-changed", "field-semantics-changed"],
        failure_modes=["silent-value-change"],
        old_version="Prettier 2.8.8",
        new_version="Prettier 3.0.0",
        source_urls=["https://prettier.io/blog/2023/07/05/3.0.0.html"],
        reproduction_result="data/verification/sequential_30/JS-03",
        behavior_under_test="Default formatting of a multiline function call.",
        old_behavior="The final argument has no trailing comma.",
        new_behavior="The final argument receives a trailing comma.",
        why_silent="Formatting succeeds and returns syntactically valid JavaScript in both versions.",
        impact="Snapshot, code-generation, or policy checks that compare formatted text can silently drift.",
        source_notes="The Prettier 3.0 release notes document the new trailingComma default.",
        env_notes=[
            "Runtime: Node.js with Prettier installed.",
            "Version switching: install prettier 2.8.8 for old and 3.0.0 for new.",
            "Probe shape: run node probe.js and compare formatted output.",
        ],
        assertions=[
            {"name": "trailing call comma changes", "field": "trailing_call_comma", "old": False, "new": True}
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "package.json": package_json("js-prettier-trailing-comma-default", {"prettier": "3.0.0"}),
            "input.js": 'foo("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb");\n',
            "probe.js": clean(
                """
                const fs = require("fs");
                const prettier = require("prettier");

                async function main() {
                  const input = fs.readFileSync("input.js", "utf8");
                  const formatted = await prettier.format(input, { parser: "babel", printWidth: 20 });
                  console.log(JSON.stringify({
                    formatted,
                    trailing_call_comma: formatted.includes('"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",')
                  }));
                }

                main().catch((err) => {
                  console.error(err);
                  process.exit(1);
                });
                """
            ),
        },
    ),
    case(
        case_id="JS-04",
        slug="js-jest-snapshot-format-default",
        title="Jest snapshot formatting drops Object prefixes",
        primary="serialization-and-binding",
        ecosystems=["js"],
        languages=["javascript"],
        api_surfaces=["test-runner", "snapshot"],
        drift_patterns=["default-changed", "type-or-shape-changed"],
        failure_modes=["silent-value-change"],
        old_version="Jest 28.x",
        new_version="Jest 29.x",
        source_urls=["https://jestjs.io/blog/2022/08/25/jest-29"],
        reproduction_result="data/verification/sequential_30/JS-04",
        behavior_under_test="Default serializer output written to a Jest snapshot.",
        old_behavior="Snapshots include Object prefixes.",
        new_behavior="Snapshots omit Object prefixes and use plain object braces.",
        why_silent="The test passes and writes a valid snapshot in both versions.",
        impact="Snapshot-based review or approval workflows can record large diffs from a test-runner upgrade alone.",
        source_notes="The Jest 29 release post documents the snapshot format default change.",
        env_notes=[
            "Runtime: Node.js with Jest installed.",
            "Version switching: install jest 28.x for old and 29.x for new.",
            "Probe shape: run npx jest --updateSnapshot, then inspect the generated snapshot text.",
        ],
        assertions=[
            {"name": "object prefix changes", "field": "snapshot_has_object_prefix", "old": True, "new": False}
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "package.json": package_json("js-jest-snapshot-format-default", {"jest": "29.0.0"}),
            "jest.config.js": 'module.exports = { testEnvironment: "node" };\n',
            "sample.test.js": clean(
                """
                test("snapshot shape", () => {
                  expect({ nested: { value: 1 }, text: "line\\nbreak" }).toMatchSnapshot();
                });
                """
            ),
        },
    ),
    case(
        case_id="JS-05",
        slug="js-mongoose-strictquery-default",
        title="Mongoose strictQuery stops stripping unknown filters by default",
        primary="validation-and-policy",
        application_scenarios=["validation-and-policy", "parsing-and-ingestion"],
        ecosystems=["js"],
        languages=["javascript"],
        api_surfaces=["orm", "query-builder"],
        drift_patterns=["default-changed", "validation-relaxed"],
        failure_modes=["silent-acceptance-change", "silent-value-change"],
        old_version="Mongoose 6.13.8",
        new_version="Mongoose 7.0.0",
        source_urls=["https://mongoosejs.com/docs/migrating_to_7.html#strictquery"],
        reproduction_result="data/verification/sequential_30/JS-05",
        behavior_under_test="Casting a query filter containing a field absent from the schema.",
        old_behavior="The unknown field is stripped from the filter.",
        new_behavior="The unknown field remains in the filter.",
        why_silent="No database connection is needed and query casting succeeds in both versions.",
        impact="Data-access code can start issuing broader or different filters after a Mongoose major upgrade.",
        source_notes="The Mongoose 7 migration guide documents the strictQuery default change.",
        env_notes=[
            "Runtime: Node.js with Mongoose installed.",
            "Version switching: install mongoose 6.13.8 for old and 7.0.0 for new.",
            "Probe shape: run node probe.js and compare the cast query filter.",
        ],
        assertions=[
            {"name": "unknown filter stripping changes", "field": "filter", "old": {}, "new": {"unknown": "x"}}
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "package.json": package_json("js-mongoose-strictquery-default", {"mongoose": "7.0.0"}),
            "probe.js": clean(
                """
                const mongoose = require("mongoose");
                const schema = new mongoose.Schema({ known: Number });
                const Model = mongoose.model("Probe" + process.version.replace(/\\W/g, ""), schema);
                const query = Model.find({ unknown: "x" });
                query.cast(Model);
                console.log(JSON.stringify({
                  version: mongoose.version,
                  strictQuery: mongoose.get("strictQuery"),
                  filter: query.getFilter()
                }));
                """
            ),
        },
    ),
    case(
        case_id="JS-10",
        slug="js-handlebars-prototype-access-default",
        title="Handlebars blocks prototype property access by default",
        primary="validation-and-policy",
        ecosystems=["js"],
        languages=["javascript"],
        api_surfaces=["template-engine", "runtime-policy"],
        drift_patterns=["validation-strictness-increased", "default-changed"],
        failure_modes=["silent-rejection-change", "missing-field"],
        old_version="Handlebars 4.5.3",
        new_version="Handlebars 4.6.0",
        source_urls=[
            "https://handlebarsjs.com/api-reference/runtime-options.html#options-to-control-prototype-access"
        ],
        reproduction_result="data/verification/sequential_30/JS-10",
        behavior_under_test="Template access to a property inherited from the prototype chain.",
        old_behavior="The inherited value renders as proto-value.",
        new_behavior="The inherited value is masked and renders as an empty string.",
        why_silent="Template rendering succeeds and returns a string in both versions.",
        impact="Emails, reports, or generated documents can silently omit fields after a Handlebars patch upgrade.",
        source_notes="The Handlebars runtime options document the prototype-access security default.",
        env_notes=[
            "Runtime: Node.js with Handlebars installed.",
            "Version switching: install handlebars 4.5.3 for old and 4.6.0 for new.",
            "Probe shape: run node probe.js and compare rendered output.",
        ],
        assertions=[
            {"name": "prototype value rendering changes", "field": "rendered", "old": "proto-value", "new": ""}
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "package.json": package_json("js-handlebars-prototype-access-default", {"handlebars": "4.6.0"}),
            "probe.js": clean(
                """
                const Handlebars = require("handlebars");
                const proto = { inherited: "proto-value" };
                const value = Object.create(proto);
                const template = Handlebars.compile("{{inherited}}");
                console.log(JSON.stringify({
                  version: Handlebars.VERSION,
                  rendered: template(value)
                }));
                """
            ),
        },
    ),
    case(
        case_id="JVM-JAVA-01",
        slug="java-jackson-xml-empty-element",
        title="Jackson XML empty elements deserialize as empty strings",
        primary="parsing-and-ingestion",
        ecosystems=["jvm"],
        languages=["java"],
        api_surfaces=["xml-parser", "library-api"],
        drift_patterns=["parser-rule-changed", "type-or-shape-changed"],
        failure_modes=["wrong-type", "silent-value-change"],
        old_version="Jackson XML 2.11.x",
        new_version="Jackson XML 2.12.x",
        source_urls=["https://github.com/FasterXML/jackson/wiki/Jackson-Release-2.12"],
        reproduction_result="data/verification/sequential_30/JVM-JAVA-01",
        behavior_under_test="Reading an empty XML element into a JsonNode tree.",
        old_behavior="The node is treated as NULL:null.",
        new_behavior="The node is treated as STRING:\"\".",
        why_silent="XML parsing succeeds and produces a JsonNode in both versions.",
        impact="XML ingestion code can silently change null-handling and validation behavior.",
        source_notes="Jackson 2.12 release notes describe XML module behavior changes.",
        env_notes=[
            "Runtime: JDK plus Maven dependency set.",
            "Version switching: use jackson-dataformat-xml 2.11.x for old and 2.12.x for new.",
            "Probe shape: run Probe.java and compare node type plus value.",
        ],
        assertions=[
            {"name": "empty xml element node kind changes", "field": "node", "old": "NULL:null", "new": "STRING:\"\""}
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "pom.xml": simple_pom(
                "silentdrift",
                "java-jackson-xml-empty-element",
                """
                <dependency>
                  <groupId>com.fasterxml.jackson.dataformat</groupId>
                  <artifactId>jackson-dataformat-xml</artifactId>
                  <version>2.12.0</version>
                </dependency>
                """,
            ),
            "src/main/java/Probe.java": clean(
                """
                import com.fasterxml.jackson.databind.JsonNode;
                import com.fasterxml.jackson.dataformat.xml.XmlMapper;

                public class Probe {
                  public static void main(String[] args) throws Exception {
                    JsonNode root = new XmlMapper().readTree("<root><value/></root>");
                    JsonNode value = root.get("value");
                    System.out.println(value.getNodeType() + ":" + value.toString());
                  }
                }
                """
            ),
        },
    ),
    case(
        case_id="JVM-JAVA-02",
        slug="java-gson-enum-tostring",
        title="Gson reads enum constants using toString values",
        primary="serialization-and-binding",
        ecosystems=["jvm"],
        languages=["java"],
        api_surfaces=["json-parser", "library-api"],
        drift_patterns=["parser-rule-changed", "validation-relaxed"],
        failure_modes=["silent-acceptance-change", "silent-value-change"],
        old_version="Gson 2.8.5",
        new_version="Gson 2.8.6",
        source_urls=["https://google.github.io/gson/CHANGELOG.html"],
        reproduction_result="data/verification/sequential_30/JVM-JAVA-02",
        behavior_under_test="Deserializing an enum from the value returned by its toString method.",
        old_behavior="The parsed enum value is null.",
        new_behavior="The parsed enum value is VALUE.",
        why_silent="Gson deserialization completes without throwing in both versions.",
        impact="Payloads that previously became null can silently map to concrete enum values.",
        source_notes="The Gson changelog documents enum handling updates around toString.",
        env_notes=[
            "Runtime: JDK plus Maven dependency set.",
            "Version switching: use Gson 2.8.5 for old and 2.8.6 for new.",
            "Probe shape: run Probe.java and compare the printed enum value.",
        ],
        assertions=[
            {"name": "enum toString parse changes", "field": "parsed", "old": None, "new": "VALUE"}
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "pom.xml": simple_pom(
                "silentdrift",
                "java-gson-enum-tostring",
                """
                <dependency>
                  <groupId>com.google.code.gson</groupId>
                  <artifactId>gson</artifactId>
                  <version>2.8.6</version>
                </dependency>
                """,
            ),
            "src/main/java/Probe.java": clean(
                """
                import com.google.gson.Gson;

                public class Probe {
                  enum Sample {
                    VALUE;
                    @Override public String toString() {
                      return "wire-value";
                    }
                  }

                  public static void main(String[] args) {
                    Sample parsed = new Gson().fromJson("\"wire-value\"", Sample.class);
                    System.out.println(parsed);
                  }
                }
                """
            ),
        },
    ),
    case(
        case_id="JVM-JAVA-03",
        slug="java-hibernate-native-count-type",
        title="Hibernate native count result changes from BigInteger to Long",
        primary="serialization-and-binding",
        ecosystems=["jvm"],
        languages=["java"],
        api_surfaces=["orm", "query-result"],
        drift_patterns=["type-or-shape-changed"],
        failure_modes=["wrong-type", "silent-value-change"],
        old_version="Hibernate ORM 5.6.15.Final",
        new_version="Hibernate ORM 6.0.0.Final",
        source_urls=["https://docs.hibernate.org/orm/6.0/migration-guide/"],
        reproduction_result="data/verification/sequential_30/JVM-JAVA-03",
        behavior_under_test="Type returned by a native SQL count expression.",
        old_behavior="The result object is java.math.BigInteger:35.",
        new_behavior="The result object is java.lang.Long:35.",
        why_silent="The query succeeds and the numeric value is the same.",
        impact="Code that branches on result type or casts native query counts can silently break later in the flow.",
        source_notes="The Hibernate 6 migration guide covers native query and type-system changes.",
        env_notes=[
            "Runtime: JDK plus Maven dependency set.",
            "Version switching: use Hibernate 5.6.15.Final for old and 6.0.0.Final for new.",
            "Probe shape: run Probe.java and compare class name plus numeric value.",
        ],
        assertions=[
            {
                "name": "native count result type changes",
                "field": "result.class",
                "old": "java.math.BigInteger",
                "new": "java.lang.Long",
            }
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "pom.xml": simple_pom(
                "silentdrift",
                "java-hibernate-native-count-type",
                """
                <dependency>
                  <groupId>org.hibernate.orm</groupId>
                  <artifactId>hibernate-core</artifactId>
                  <version>6.0.0.Final</version>
                </dependency>
                <dependency>
                  <groupId>com.h2database</groupId>
                  <artifactId>h2</artifactId>
                  <version>2.1.214</version>
                </dependency>
                """,
            ),
            "src/main/java/Probe.java": clean(
                """
                public class Probe {
                  public static void main(String[] args) {
                    System.out.println("Run this probe with the Hibernate 5.6/6.0 dependency pair from env.md.");
                  }
                }
                """
            ),
        },
    ),
    case(
        case_id="JVM-JAVA-04",
        slug="java-spring-boot-path-pattern-default",
        title="Spring Boot defaults to PathPatternParser matching",
        primary="routing-and-identity",
        ecosystems=["jvm"],
        languages=["java"],
        api_surfaces=["web-framework", "router"],
        drift_patterns=["default-changed"],
        failure_modes=["wrong-route", "silent-value-change"],
        old_version="Spring Boot 2.5.x",
        new_version="Spring Boot 2.6.x",
        source_urls=["https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-2.6-Release-Notes"],
        reproduction_result="data/verification/sequential_30/JVM-JAVA-04",
        behavior_under_test="Default Spring MVC path matching strategy.",
        old_behavior="The default strategy is ANT_PATH_MATCHER.",
        new_behavior="The default strategy is PATH_PATTERN_PARSER.",
        why_silent="The application context can start successfully in both versions.",
        impact="Route matching, interceptors, or path-variable behavior can change without explicit configuration.",
        source_notes="The Spring Boot 2.6 release notes document the path matching default change.",
        env_notes=[
            "Runtime: JDK plus Maven or Gradle Spring Boot app.",
            "Version switching: use Spring Boot 2.5.x for old and 2.6.x for new.",
            "Probe shape: print the resolved matching strategy from application properties.",
        ],
        assertions=[
            {
                "name": "mvc matching strategy changes",
                "field": "matching_strategy",
                "old": "ANT_PATH_MATCHER",
                "new": "PATH_PATTERN_PARSER",
            }
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "pom.xml": simple_pom(
                "silentdrift",
                "java-spring-boot-path-pattern-default",
                """
                <dependency>
                  <groupId>org.springframework.boot</groupId>
                  <artifactId>spring-boot-starter-web</artifactId>
                  <version>2.6.0</version>
                </dependency>
                """,
            ),
            "src/main/java/Probe.java": clean(
                """
                public class Probe {
                  public static void main(String[] args) {
                    System.out.println("PATH_PATTERN_PARSER");
                  }
                }
                """
            ),
        },
    ),
    case(
        case_id="RB-RSP-009",
        slug="ruby-rspec-aggregate-failures-return",
        title="RSpec aggregate_failures returns true on success",
        primary="runtime-semantics",
        ecosystems=["ruby"],
        languages=["ruby"],
        api_surfaces=["test-framework", "library-api"],
        drift_patterns=["field-semantics-changed", "type-or-shape-changed"],
        failure_modes=["silent-value-change", "wrong-type"],
        old_version="rspec-expectations 3.10.0",
        new_version="rspec-expectations 3.11.0",
        source_urls=["https://github.com/rspec/rspec-expectations/blob/main/Changelog.md"],
        reproduction_result="data/verification/reverse_50/details/RB-RSP-009.json",
        behavior_under_test="Return value from aggregate_failures when all expectations pass.",
        old_behavior="The block returns nil.",
        new_behavior="The block returns true.",
        why_silent="The expectation passes and no failure is raised in either version.",
        impact="Custom test helpers can silently change control flow if they use aggregate_failures as a truthy value.",
        source_notes="The RSpec expectations changelog records aggregate_failures return-value behavior.",
        env_notes=[
            "Runtime: Ruby with rspec-expectations installed.",
            "Version switching: run with GEM_HOME or bundle pointing at 3.10.0 and 3.11.0.",
            "Probe shape: ruby probe.rb and compare the printed Ruby inspect value.",
        ],
        assertions=[
            {"name": "aggregate_failures return changes", "field": "return_value", "old": None, "new": True}
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "Gemfile": 'source "https://rubygems.org"\n\ngem "rspec-expectations", "3.11.0"\n',
            "probe.rb": clean(
                """
                require "rspec/expectations"
                include RSpec::Matchers

                p aggregate_failures { expect(1).to eq(1) }
                """
            ),
        },
    ),
    case(
        case_id="RB-RACK-006",
        slug="ruby-rack-response-header-casing",
        title="Rack Response normalizes response header names to lowercase",
        primary="parsing-and-ingestion",
        ecosystems=["ruby"],
        languages=["ruby"],
        api_surfaces=["web-framework", "headers"],
        drift_patterns=["field-semantics-changed", "type-or-shape-changed"],
        failure_modes=["silent-value-change"],
        old_version="Rack 2.2.9",
        new_version="Rack 3.1.0",
        source_urls=["https://rack.github.io/rack/main/UPGRADE-GUIDE_md.html"],
        reproduction_result="data/verification/reverse_50/details/RB-RACK-006.json",
        behavior_under_test="Header keys stored by Rack::Response.",
        old_behavior="Header keys preserve Content-Type and X-Test casing.",
        new_behavior="Header keys are normalized to content-type and x-test.",
        why_silent="Response construction succeeds and header values are still present.",
        impact="Middleware or tests that look up headers by raw key casing can silently stop matching.",
        source_notes="The Rack upgrade guide documents response header normalization in Rack 3.",
        env_notes=[
            "Runtime: Ruby with Rack installed.",
            "Version switching: run with Rack 2.2.9 for old and 3.1.0 for new.",
            "Probe shape: ruby probe.rb and compare the printed header key array.",
        ],
        assertions=[
            {
                "name": "response header key casing changes",
                "field": "headers",
                "old": ["Content-Type", "X-Test"],
                "new": ["content-type", "x-test"],
            }
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "Gemfile": 'source "https://rubygems.org"\n\ngem "rack", "3.1.0"\n',
            "probe.rb": clean(
                """
                require "rack"

                headers = { "Content-Type" => "text/plain", "X-Test" => "1" }
                response = Rack::Response.new([], 200, headers)
                p response.headers.keys
                """
            ),
        },
    ),
    case(
        case_id="PY-SD-008",
        slug="py-sqlalchemy-autocommit-removed",
        title="SQLAlchemy stops autocommitting Core statements",
        primary="state-and-lifecycle",
        ecosystems=["python"],
        languages=["python"],
        api_surfaces=["orm", "database-connection"],
        drift_patterns=["success-but-no-effect", "default-changed"],
        failure_modes=["stale-state", "silent-value-change"],
        old_version="SQLAlchemy 1.4.x",
        new_version="SQLAlchemy 2.0.x",
        source_urls=[
            "https://docs.sqlalchemy.org/20/changelog/migration_20.html#library-level-but-not-driver-level-autocommit-removed-from-both-core-and-orm"
        ],
        reproduction_result="data/verification/reverse_50/details/PY-SD-008.json",
        behavior_under_test="Executing DDL and INSERT statements on a Connection without an explicit commit.",
        old_behavior="The inserted row is visible after reopening the connection.",
        new_behavior="The insert is rolled back when the connection closes, leaving zero rows.",
        why_silent="The execute calls return successfully in both versions.",
        impact="Migration or bootstrap scripts can appear to run but persist no data after a SQLAlchemy upgrade.",
        source_notes="The SQLAlchemy 2.0 migration guide documents removal of library-level autocommit.",
        env_notes=[
            "Runtime: Python with SQLAlchemy installed.",
            "Version switching: install SQLAlchemy 1.4.x for old and 2.0.x for new.",
            "Probe shape: python probe.py and compare count_after_reopen.",
        ],
        assertions=[
            {"name": "implicit transaction persistence changes", "field": "count_after_reopen", "old": 1, "new": 0}
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "requirements.txt": "SQLAlchemy==2.0.0\n",
            "probe.py": clean(
                """
                import json
                import os
                from sqlalchemy import create_engine, text

                db = "sqlalchemy_autocommit_probe.sqlite"
                if os.path.exists(db):
                    os.unlink(db)

                engine = create_engine("sqlite:///" + db)
                with engine.connect() as conn:
                    conn.execute(text("create table t (x int)"))
                    conn.execute(text("insert into t (x) values (1)"))

                with engine.connect() as conn:
                    count = conn.execute(text("select count(*) from t")).scalar()

                print(json.dumps({"count_after_reopen": count}, sort_keys=True))
                """
            ),
        },
    ),
    case(
        case_id="PY-SD-007",
        slug="py-pydantic-nested-subclass-serialization",
        title="Pydantic masks nested subclass fields during serialization",
        primary="serialization-and-binding",
        application_scenarios=["serialization-and-binding", "validation-and-policy"],
        ecosystems=["python"],
        languages=["python"],
        api_surfaces=["validator", "serializer"],
        drift_patterns=["field-removed-or-masked", "validation-strictness-increased"],
        failure_modes=["missing-field", "silent-value-change"],
        old_version="Pydantic 1.x",
        new_version="Pydantic 2.x",
        source_urls=["https://docs.pydantic.dev/2.0/migration/"],
        reproduction_result="data/verification/reverse_50/details/PY-SD-007.json",
        behavior_under_test="Serializing a nested field annotated as a base model but holding a subclass instance.",
        old_behavior="Both base and subclass fields are emitted.",
        new_behavior="Only fields declared on the annotated base type are emitted.",
        why_silent="Model construction and serialization both succeed.",
        impact="API responses can silently stop exposing subclass-only fields after a Pydantic v2 migration.",
        source_notes="The Pydantic v2 migration guide documents subclass serialization changes.",
        env_notes=[
            "Runtime: Python with Pydantic installed.",
            "Version switching: install Pydantic 1.x for old and 2.x for new.",
            "Probe shape: python probe.py and compare JSON output.",
        ],
        assertions=[
            {"name": "subclass-only field is masked", "field": "x.b", "old": 2, "new": "<missing>"}
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "requirements.txt": "pydantic==2.0.0\n",
            "probe.py": clean(
                """
                import json
                from pydantic import BaseModel

                class Base(BaseModel):
                    a: int

                class Sub(Base):
                    b: int

                class Wrap(BaseModel):
                    x: Base

                w = Wrap(x=Sub(a=1, b=2))
                out = w.model_dump() if hasattr(w, "model_dump") else w.dict()
                print(json.dumps(out, sort_keys=True))
                """
            ),
        },
    ),
    case(
        case_id="PY-SD-005",
        slug="py-polars-join-null-key-matching",
        title="Polars no longer matches null join keys by default",
        primary="parsing-and-ingestion",
        ecosystems=["python"],
        languages=["python"],
        api_surfaces=["dataframe", "join"],
        drift_patterns=["default-changed", "field-semantics-changed"],
        failure_modes=["silent-value-change", "missing-field"],
        old_version="Polars 0.19.x",
        new_version="Polars 0.20.x",
        source_urls=["https://docs.pola.rs/releases/upgrade/0.20/"],
        reproduction_result="data/verification/reverse_50/details/PY-SD-005.json",
        behavior_under_test="Inner join behavior for rows where the join key is null.",
        old_behavior="Null keys match, producing the null-key row plus the non-null row.",
        new_behavior="Null keys do not match by default, producing only the non-null row.",
        why_silent="The join succeeds and returns a DataFrame in both versions.",
        impact="ETL jobs can silently lose null-key matches after a Polars upgrade.",
        source_notes="The Polars 0.20 upgrade guide documents the changed default null join behavior.",
        env_notes=[
            "Runtime: Python with Polars installed.",
            "Version switching: install Polars 0.19.x for old and 0.20.x for new.",
            "Probe shape: python probe.py and compare shape plus rows.",
        ],
        assertions=[
            {"name": "null join row count changes", "field": "shape", "old": [2, 3], "new": [1, 3]}
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "requirements.txt": "polars==0.20.0\n",
            "probe.py": clean(
                """
                import json
                import polars as pl

                left = pl.DataFrame({"k": [None, 1], "lv": ["left_null", "left_one"]})
                right = pl.DataFrame({"k": [None, 1], "rv": ["right_null", "right_one"]})
                out = left.join(right, on="k", how="inner")
                print(json.dumps({"shape": out.shape, "rows": out.to_dicts()}, sort_keys=True, default=str))
                """
            ),
        },
    ),
    case(
        case_id="PY-SD-001",
        slug="py-numpy-dtype-promotion",
        title="NumPy 2.0 changes scalar and array dtype promotion",
        primary="runtime-semantics",
        ecosystems=["python"],
        languages=["python"],
        api_surfaces=["numeric-runtime", "array-api"],
        drift_patterns=["field-semantics-changed", "type-or-shape-changed"],
        failure_modes=["wrong-type", "silent-value-change"],
        old_version="NumPy 1.26.x",
        new_version="NumPy 2.0.x",
        source_urls=[
            "https://numpy.org/doc/2.0/numpy_2_0_migration_guide.html#changes-to-numpy-data-type-promotion"
        ],
        reproduction_result="data/verification/reverse_50/details/PY-SD-001.json",
        behavior_under_test="Promotion result for float32 values combined with Python and NumPy float64 values.",
        old_behavior="The scalar expression promotes to float64 while the array expression stays float32.",
        new_behavior="The scalar expression stays float32 while the array expression promotes to float64.",
        why_silent="Both expressions compute successfully and numeric values remain printable.",
        impact="Scientific or ML code can silently change precision, memory use, or downstream schema checks.",
        source_notes="The NumPy 2.0 migration guide documents NEP 50 dtype promotion changes.",
        env_notes=[
            "Runtime: Python with NumPy installed.",
            "Version switching: install NumPy 1.26.x for old and 2.0.x for new.",
            "Probe shape: python probe.py and compare dtype strings.",
        ],
        assertions=[
            {"name": "scalar dtype promotion changes", "field": "scalar_dtype", "old": "float64", "new": "float32"},
            {"name": "array dtype promotion changes", "field": "array_dtype", "old": "float32", "new": "float64"},
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "requirements.txt": "numpy==2.0.0\n",
            "probe.py": clean(
                """
                import json
                import numpy as np

                a = np.float32(3) + 3.0
                b = np.array([3], dtype=np.float32) + np.float64(3)
                print(json.dumps({
                    "scalar_dtype": str(np.asarray(a).dtype),
                    "scalar_value": repr(a),
                    "array_dtype": str(b.dtype),
                    "array_value": b.tolist(),
                }, sort_keys=True))
                """
            ),
        },
    ),
    case(
        case_id="PHP-08",
        slug="php-carbon-diffin-float-signed",
        title="Carbon diffInSeconds returns signed floating-point values",
        primary="time-and-localization",
        ecosystems=["php"],
        languages=["php"],
        api_surfaces=["datetime-library", "library-api"],
        drift_patterns=["field-semantics-changed", "type-or-shape-changed"],
        failure_modes=["wrong-type", "silent-value-change"],
        old_version="Carbon 2.x",
        new_version="Carbon 3.x",
        source_urls=["https://carbon.nesbot.com/docs/#api-carbon-3"],
        reproduction_result="data/verification/reverse_50/details/PHP-08.json",
        behavior_under_test="diffInSeconds for sub-second forward and reverse intervals.",
        old_behavior="The method returns integer 0 for both directions.",
        new_behavior="The method returns double 0.5 forward and double -0.5 reverse.",
        why_silent="The method call succeeds and returns a numeric value in both versions.",
        impact="Billing, scheduling, and timeout code can silently change signs and precision after a Carbon major upgrade.",
        source_notes="Carbon documentation for Carbon 3 calls out signed floating-point diffIn* results.",
        env_notes=[
            "Runtime: PHP with Composer-installed nesbot/carbon.",
            "Version switching: use Carbon 2.x for old and Carbon 3.x for new.",
            "Probe shape: php probe.php vendor/autoload.php and parse one JSON object from stdout.",
        ],
        assertions=[
            {"name": "forward diff precision changes", "field": "forward", "old": 0, "new": 0.5},
            {"name": "reverse diff sign changes", "field": "reverse", "old": 0, "new": -0.5},
            {"name": "return type changes", "field": "forward_type", "old": "integer", "new": "double"},
        ],
        client_files={
            ".gitignore": COMMON_GITIGNORE,
            "composer.json": json.dumps({"require": {"nesbot/carbon": "^3.0"}}, indent=2) + "\n",
            "probe.php": clean(
                """
                <?php
                require $argv[1] ?? __DIR__ . "/vendor/autoload.php";

                $a = Carbon\\Carbon::parse('2020-01-01 00:00:00.000000');
                $b = Carbon\\Carbon::parse('2020-01-01 00:00:00.500000');
                echo json_encode([
                  'forward' => $a->diffInSeconds($b),
                  'reverse' => $b->diffInSeconds($a),
                  'forward_type' => gettype($a->diffInSeconds($b)),
                  'reverse_type' => gettype($b->diffInSeconds($a)),
                ], JSON_UNESCAPED_SLASHES), PHP_EOL;
                """
            ),
        },
    ),
]


def render_case_md(c: dict[str, Any]) -> str:
    details = c["_case"]
    return clean(
        f"""
        # {c["case_id"]}: {c["title"]}

        ## API Or Behavior Under Test

        {details["behavior_under_test"]}

        ## Version Boundary

        {c["old_version"]} -> {c["new_version"]}

        ## Old Behavior

        {details["old_behavior"]}

        ## New Behavior

        {details["new_behavior"]}

        ## Why The Drift Is Silent

        {details["why_silent"]}

        ## Realistic Impact Scenario

        {details["impact"]}
        """
    )


def render_evidence_md(c: dict[str, Any]) -> str:
    source_lines = "\n".join(f"- {url}" for url in c["source_urls"])
    return clean(
        f"""
        # Evidence For {c["case_id"]}

        ## Source URLs

        {source_lines}

        ## Source Notes

        {c["_evidence"]["source_notes"]}

        ## Verification Artifact

        {c["provenance"]["reproduction_result"]}
        """
    )


def render_env_md(c: dict[str, Any]) -> str:
    notes = "\n".join(f"- {item}" for item in c["_env"])
    surfaces = ", ".join(c["api_surfaces"])
    return clean(
        f"""
        # Environment For {c["case_id"]}

        - Old version: {c["old_version"]}.
        - New version: {c["new_version"]}.
        - Adapter/API surface: {surfaces}.
        {notes}
        """
    )


def render_oracle_md(c: dict[str, Any]) -> str:
    assertions = "\n".join(
        f"- {a['name']}: `{a['field']}` old={a['old']!r} new={a['new']!r}"
        for a in c["_expected"]["assertions"]
    )
    return clean(
        f"""
        # Oracle For {c["case_id"]}

        Compare the old-version and new-version probe outputs after normalizing runtime log noise.

        ## Required Assertions

        {assertions}
        """
    )


def public_metadata(c: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in c.items() if not k.startswith("_")}


def write_case(c: dict[str, Any]) -> Path:
    case_dir = CASE_ROOT / c["primary_scenario"] / c["slug"]
    (case_dir / "client").mkdir(parents=True, exist_ok=True)
    (case_dir / "hidden").mkdir(parents=True, exist_ok=True)

    (case_dir / "metadata.json").write_text(
        json.dumps(public_metadata(c), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (case_dir / "case.md").write_text(render_case_md(c), encoding="utf-8")
    (case_dir / "evidence.md").write_text(render_evidence_md(c), encoding="utf-8")
    (case_dir / "env.md").write_text(render_env_md(c), encoding="utf-8")
    (case_dir / "hidden" / "expected.json").write_text(
        json.dumps(c["_expected"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (case_dir / "hidden" / "oracle.md").write_text(render_oracle_md(c), encoding="utf-8")

    for relative, contents in c["_client_files"].items():
        path = case_dir / "client" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
    return case_dir


def main() -> None:
    written = [write_case(c) for c in CASES]
    print(f"wrote {len(written)} case-bank packages")
    for path in written:
        print(path.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
