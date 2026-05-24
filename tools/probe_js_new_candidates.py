from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRATCH = ROOT / "data" / "verification" / "js_new_probe"
NPM = shutil.which("npm.cmd") or shutil.which("npm") or "npm.cmd"
NODE = shutil.which("node.exe") or shutil.which("node") or "node"


@dataclass(frozen=True)
class Candidate:
    slug: str
    package: str
    old: str
    new: str
    source: str
    client: str
    module_type: str = "commonjs"


CANDIDATES = [
    Candidate(
        slug="js-semver-coerce-include-prerelease",
        package="semver",
        old="7.5.4",
        new="7.6.0",
        source="https://github.com/npm/node-semver/releases/tag/v7.6.0",
        client=r'''const semver = require("semver");
const version = semver.coerce("prefix 1.2.3-beta.4+build.5", { includePrerelease: true });
console.log(JSON.stringify({ version: version && version.version }));
''',
    ),
    Candidate(
        slug="js-date-fns-overlap-sorted-inclusive",
        package="date-fns",
        old="3.0.5",
        new="3.0.6",
        source="https://github.com/date-fns/date-fns/releases/tag/v3.0.6",
        client=r'''const { areIntervalsOverlapping } = require("date-fns");
const left = { start: new Date("2020-01-10T00:00:00Z"), end: new Date("2020-01-01T00:00:00Z") };
const right = { start: new Date("2020-01-05T00:00:00Z"), end: new Date("2020-01-05T00:00:00Z") };
console.log(JSON.stringify({ overlapping: areIntervalsOverlapping(left, right, { inclusive: true }) }));
''',
    ),
    Candidate(
        slug="js-htmlparser2-textarea-special-tag",
        package="htmlparser2",
        old="9.0.0",
        new="9.1.0",
        source="https://github.com/fb55/htmlparser2/releases/tag/v9.1.0",
        client=r'''const { parseDocument } = require("htmlparser2");
const textarea = parseDocument("<textarea><b>x</b></textarea>").children[0];
const child = textarea.children[0];
console.log(JSON.stringify({
  childType: child.type,
  childName: child.name || null,
  childData: child.data || null
}));
''',
    ),
    Candidate(
        slug="js-ajv-jtd-optional-leading-comma",
        package="ajv",
        old="8.11.2",
        new="8.12.0",
        source="https://github.com/ajv-validator/ajv/releases/tag/v8.12.0",
        client=r'''const AjvJTD = require("ajv/dist/jtd").default;
const ajv = new AjvJTD();
const serialize = ajv.compileSerializer({
  optionalProperties: {
    a: { type: "int32" },
    b: { type: "int32" }
  }
});
console.log(JSON.stringify({ serialized: serialize({ b: 1 }) }));
''',
    ),
    Candidate(
        slug="js-query-string-encoded-separator-array",
        package="query-string",
        old="9.2.2",
        new="9.3.0",
        source="https://github.com/sindresorhus/query-string/releases/tag/v9.3.0",
        module_type="module",
        client=r'''import queryString from "query-string";
const parsed = queryString.parse("ids=1%7C2", { arrayFormat: "separator", arrayFormatSeparator: "|" });
console.log(JSON.stringify({ ids: parsed.ids, isArray: Array.isArray(parsed.ids) }));
''',
    ),
    Candidate(
        slug="js-validator-leading-zero-port",
        package="validator",
        old="13.11.0",
        new="13.12.0",
        source="https://github.com/validatorjs/validator.js/releases/tag/13.12.0",
        client=r'''const validator = require("validator");
console.log(JSON.stringify({
  port01: validator.isPort("01"),
  port00080: validator.isPort("00080"),
  port80: validator.isPort("80")
}));
''',
    ),
    Candidate(
        slug="js-whatwg-url-caret-percent-encoding",
        package="whatwg-url",
        old="14.1.1",
        new="14.2.0",
        source="https://github.com/jsdom/whatwg-url/releases/tag/v14.2.0",
        client=r'''const { URL } = require("whatwg-url");
const url = new URL("https://example.test/a^b?x=1^2");
console.log(JSON.stringify({ href: url.href, pathname: url.pathname, search: url.search }));
''',
    ),
    Candidate(
        slug="js-is-core-module-node-test-registry",
        package="is-core-module",
        old="2.8.1",
        new="2.9.0",
        source="https://github.com/inspect-js/is-core-module/blob/main/CHANGELOG.md",
        client=r'''const isCore = require("is-core-module");
console.log(JSON.stringify({
  nodeTest18: isCore("node:test", "18.0.0"),
  nodeTest16: isCore("node:test", "16.0.0")
}));
''',
    ),
    Candidate(
        slug="js-cookie-partitioned-serialize-option",
        package="cookie",
        old="0.5.0",
        new="0.6.0",
        source="https://github.com/jshttp/cookie/releases/tag/v0.6.0",
        client=r'''const cookie = require("cookie");
const text = cookie.serialize("sid", "abc", { partitioned: true, secure: true, sameSite: "none" });
console.log(JSON.stringify({ text, hasPartitioned: text.includes("Partitioned") }));
''',
    ),
    Candidate(
        slug="js-mime-db-parquet-media-type",
        package="mime-db",
        old="1.52.0",
        new="1.53.0",
        source="https://github.com/jshttp/mime-db/blob/v1.53.0/db.json",
        client=r'''const db = require("mime-db");
const entry = db["application/vnd.apache.parquet"] || null;
console.log(JSON.stringify({ exists: !!entry, extensions: entry && entry.extensions ? entry.extensions : null }));
''',
    ),
    Candidate(
        slug="js-spdx-license-ids-pkgconf-added",
        package="spdx-license-ids",
        old="3.0.17",
        new="3.0.18",
        source="https://github.com/jslicense/spdx-license-ids/blob/v3.0.18/index.json",
        client=r'''const ids = require("spdx-license-ids");
console.log(JSON.stringify({ hasPkgconf: ids.includes("pkgconf"), count: ids.length }));
''',
    ),
    Candidate(
        slug="js-set-cookie-parser-partitioned-attribute",
        package="set-cookie-parser",
        old="2.6.0",
        new="2.7.0",
        source="https://github.com/nfriedly/set-cookie-parser/blob/master/README.md",
        client=r'''const setCookie = require("set-cookie-parser");
const parsed = setCookie.parse("sid=abc; Secure; SameSite=None; Partitioned")[0];
console.log(JSON.stringify({
  partitioned: parsed.partitioned === true,
  secure: parsed.secure === true,
  sameSite: parsed.sameSite || parsed.samesite || null
}));
''',
    ),
    Candidate(
        slug="js-builtin-modules-node-ffi-added",
        package="builtin-modules",
        old="5.1.0",
        new="5.2.0",
        source="https://github.com/sindresorhus/builtin-modules/releases/tag/v5.2.0",
        module_type="module",
        client=r'''import builtinModules from "builtin-modules";
console.log(JSON.stringify({ hasNodeFfi: builtinModules.includes("node:ffi"), count: builtinModules.length }));
''',
    ),
]


def main() -> int:
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir(parents=True)
    kept: list[str] = []
    for candidate in CANDIDATES:
        result = probe(candidate)
        print(json.dumps(result, sort_keys=True), flush=True)
        if (
            result["old_exit"] == 0
            and result["new_exit"] == 0
            and result["old_stderr"] == ""
            and result["new_stderr"] == ""
            and result["old_stdout"] != result["new_stdout"]
        ):
            kept.append(candidate.slug)
    print(json.dumps({"kept": kept, "kept_count": len(kept)}, sort_keys=True), flush=True)
    return 0


def probe(candidate: Candidate) -> dict[str, object]:
    result: dict[str, object] = {
        "slug": candidate.slug,
        "package": candidate.package,
        "old": candidate.old,
        "new": candidate.new,
        "source": candidate.source,
    }
    for side, version in (("old", candidate.old), ("new", candidate.new)):
        work = SCRATCH / candidate.slug / side
        work.mkdir(parents=True, exist_ok=True)
        package_json: dict[str, object] = {
            "private": True,
            "dependencies": {candidate.package: version},
        }
        if candidate.module_type == "module":
            package_json["type"] = "module"
        (work / "package.json").write_text(json.dumps(package_json, indent=2) + "\n", encoding="utf-8")
        probe_name = "probe.mjs" if candidate.module_type == "module" else "probe.js"
        (work / probe_name).write_text(candidate.client, encoding="utf-8")
        install = subprocess.run(
            [NPM, "install", "--silent", "--no-audit", "--fund=false"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            timeout=240,
        )
        if install.returncode != 0:
            result[f"{side}_exit"] = install.returncode
            result[f"{side}_stdout"] = install.stdout.strip()
            result[f"{side}_stderr"] = install.stderr.strip()
            continue
        run = subprocess.run(
            [NODE, probe_name],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
        result[f"{side}_exit"] = run.returncode
        result[f"{side}_stdout"] = run.stdout.strip()
        result[f"{side}_stderr"] = run.stderr.strip()
    return result


if __name__ == "__main__":
    raise SystemExit(main())
