# Python narrow-silent verification run - 2026-05-23

Scope: continue Python discovery using the narrowest silent-drift packaging
policy. Count only cases that are directly reviewable:

- Same public user-facing call shape.
- Both old and new runs exit successfully.
- No warning/no exception signal is needed for the observed difference.
- Patch or narrow minor release preferred.
- Official changelog/source supports the exact behavior.
- Not already accepted in the local Python drift bank.

## Direct-submit strict accepted

Strict direct-submit count from this run: **4**.

### ACCEPTED-20260523-094: beautifulsoup4 script tag get_text returns tag-local text

- Package: `beautifulsoup4`
- Versions verified: old `4.9.3`, new `4.10.0`
- API surface: `BeautifulSoup(...).script.get_text()` and parent
  `Tag.get_text(...)`
- Source:
  - https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.html?highlight=select#get-text
  - https://bugs.launchpad.net/bugs/1906226
- Local probe:
  - Input HTML:
    `<div><script>var token = 1;</script><p>Hello</p></div>`
  - Old output:
    `{"div_text": "Hello", "package": "beautifulsoup4", "script_text": "", "version": "4.9.3"}`
  - New output:
    `{"div_text": "Hello", "package": "beautifulsoup4", "script_text": "var token = 1;", "version": "4.10.0"}`
- Why it passes strict silent:
  The same parser and public tag method return normally in both versions. The
  parent `div.get_text("|")` still omits script text, but the direct
  `script.get_text()` result changes from empty to the script body.

### ACCEPTED-20260523-095: coverage JSON report stops counting module docstrings as executed

- Package: `coverage`
- Versions verified: old `7.13.0`, new `7.13.1`
- API surface: `coverage.Coverage`, `Coverage.json_report`
- Source:
  - https://coverage.readthedocs.io/en/latest/changes.html#version-7-13-1-2025-12-28
- Local probe:
  - Temporary module text:
    `"""module docs"""\nvalue = 42\n`
  - Old output:
    `{"executed_lines": [1, 2], "package": "coverage", "summary": {"covered_lines": 1, "excluded_lines": 0, "missing_lines": 0, "num_statements": 1, "percent_covered": 100.0, "percent_covered_display": "100", "percent_statements_covered": 100.0, "percent_statements_covered_display": "100"}, "version": "7.13.0"}`
  - New output:
    `{"executed_lines": [2], "package": "coverage", "summary": {"covered_lines": 1, "excluded_lines": 0, "missing_lines": 0, "num_statements": 1, "percent_covered": 100.0, "percent_covered_display": "100", "percent_statements_covered": 100.0, "percent_statements_covered_display": "100"}, "version": "7.13.1"}`
- Why it passes strict silent:
  Coverage collection and JSON reporting succeed in both versions. Downstream
  tools reading `executed_lines` silently lose the module-docstring line while
  the summary remains unchanged.

### ACCEPTED-20260523-096: json5 int subclass serialization stops using custom str

- Package: `json5`
- Versions verified: old `0.9.8`, new `0.9.9`
- API surface: `json5.dumps`
- Source:
  - https://github.com/dpranke/pyjson5
  - https://pypi.org/project/json5/
- Local probe:
  - Fixture:
    `class OddInt(int): def __str__(self): return "not-json5-number"`
  - Old output:
    `{"package": "json5", "text": "{n: not-json5-number}", "version": "0.9.8"}`
  - New output:
    `{"package": "json5", "text": "{n: 7}", "version": "0.9.9"}`
- Why it passes strict silent:
  Both versions serialize successfully through the same `json5.dumps` call.
  The old version emits an invalid numeric token derived from `__str__`; the
  new version emits the integer representation.
- Note:
  The initially queued `0.12.0 -> 0.12.1` custom-encoder indentation lead did
  not reproduce with the tested fixture, but the official issue-backed
  `0.9.8 -> 0.9.9` int-subclass fix does.

### ACCEPTED-20260523-097: filelock logger level is no longer set on import

- Package: `filelock`
- Versions verified: old `3.3.0`, new `3.3.1`
- API surface: importing `filelock`, then inspecting `logging.getLogger("filelock")`
- Source:
  - https://py-filelock.readthedocs.io/en/latest/changelog.html#v3-3-1-2021-10-15
- Local probe:
  - Fixture sets root logging to `INFO`, imports `filelock`, then prints the
    package logger level and `isEnabledFor(DEBUG)`.
  - Old output:
    `{"debug_enabled": true, "effective_level": 10, "level": 10, "package": "filelock", "version": "3.3.0"}`
  - New output:
    `{"debug_enabled": false, "effective_level": 20, "level": 0, "package": "filelock", "version": "3.3.1"}`
- Why it passes strict silent:
  The import succeeds without warning in both versions. The package logger stops
  overriding the ambient logging configuration, so debug log filtering changes
  under the same user setup.

## Verified but not counted in strict direct-submit total

### HOLD-20260523-A: Flask session cookie domain stops falling back to SERVER_NAME

- Versions tested: `Flask==2.2.5` with `Werkzeug==2.2.3` vs `Flask==2.3.0`
  with `Werkzeug==2.3.8`
- Source:
  - https://flask.palletsprojects.com/en/stable/changes/
  - https://flask.palletsprojects.com/config/#SESSION_COOKIE_DOMAIN
- Local result:
  - Old `Set-Cookie` included `Domain=.example.test`.
  - New `Set-Cookie` omitted `Domain=...`.
- Hold reason:
  The behavior is real and silent, but Flask `2.3.0` is a broad release with
  several removals and migration-adjacent changes. Do not count it under the
  narrowest "no-brainer" package-send criterion.

### HOLD-20260523-B: Docutils HTML5 footnote list gains wrapper aside

- Versions tested: old `0.18.1`, new `0.19`
- Source:
  - https://docutils.sourceforge.io/RELEASE-NOTES.html#release-0-19-2022-07-05
- Local result:
  The same `publish_parts(..., writer_name="html5")` call succeeded in both
  versions. The new body wraps footnotes in `<aside class="footnote-list ...">`.
- Hold reason:
  The diff is deterministic and local, but the source places it under
  "Output changes"; keep it available as a lower-tier candidate, not a strict
  direct-submit item.

### HOLD-20260523-C: Arrow timezone implementation changes to ZoneInfo

- Versions tested: old `1.3.0`, new `1.4.0`
- Source:
  - https://arrow.readthedocs.io/en/stable/
- Local result:
  `arrow.get(..., tzinfo="America/New_York").tzinfo` changed from a
  `dateutil.tz.tzfile` object to `zoneinfo.ZoneInfo`.
- Hold reason:
  The observed fixture only changes implementation type/repr while the tested
  offset and shift result stayed the same. Find a stronger behavioral fixture
  before promotion.

## Rejected leads from this run

### REJECTED-20260523-A: Hypothesis .gitignore side effect did not reproduce

- Versions tested: old `6.151.14`, new `6.152.0`
- Source:
  - https://hypothesis.readthedocs.io/en/latest/changelog.html
- Rejected because:
  Touching a `DirectoryBasedExampleDatabase` in a temporary directory produced
  the same entries in both versions and no `.gitignore` file in either version.

### REJECTED-20260523-B: fsspec local-file cache fixture bypassed changed cache layer

- Versions tested: old `0.8.7`, new `0.9.0`
- Source:
  - https://filesystem-spec.readthedocs.io/en/latest/changelog.html
- Rejected because:
  `fsspec.open(local_path, mode="rb").open()` returned `LocalFileOpener` with
  no observable cache object in both versions. Do not promote unless a public
  remote-like filesystem fixture reproduces the default cache change without
  internal-only hooks.

### REJECTED-20260523-C: json5 0.12.0 -> 0.12.1 indentation fixture found no diff

- Versions tested: old `0.12.0`, new `0.12.1`
- Source:
  - https://pypi.org/project/json5/
- Rejected because:
  The tested subclass-number fixture returned identical pretty output across
  `0.12.0 -> 0.12.1`. Use the verified `0.9.8 -> 0.9.9` int-subclass case
  instead.
