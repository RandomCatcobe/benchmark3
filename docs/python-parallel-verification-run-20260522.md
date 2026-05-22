# Python Parallel Verification Run - 2026-05-22

This note records the Python silent-drift search requested on 2026-05-22:
search candidates, start parallel local verification after each group of four,
and stop only after at least 10 acceptable cases are found.

## Result

- Acceptable local probes found: 14
- Strict non-yanked acceptable probes: 12
- Reproducibility shape: all accepted probes run locally, install old and new
  package versions, keep the same public call shape, exit 0, and show changed
  stdout or changed returned/serialized text.
- Yanked but real drift evidence: `click==8.2.2`, `multidict==6.3.0`.
  These are useful evidence, but excluded from the strict non-yanked count.

## Accepted Probes

| ID | Package | Versions | Probe | Old output | New output | Source |
| --- | --- | --- | --- | --- | --- | --- |
| PY-PV-20260522-001 | `jinja2` | `3.0.3 -> 3.1.0` | `groupby` default in template rendering | `CA:1;NY:1;ca:1;` | `CA:2;NY:1;` | https://jinja.palletsprojects.com/en/stable/changes/#version-3-1-0 |
| PY-PV-20260522-002 | `werkzeug` | `2.2.3 -> 2.3.0` | `werkzeug.http.dump_cookie("sid", "abc")` | `sid=abc; Path=/` | `sid=abc` | https://werkzeug.palletsprojects.com/en/stable/changes/#version-2-3-0 |
| PY-PV-20260522-003 | `starlette` | `0.17.1 -> 0.18.0` | `FileResponse.chunk_size` | `4096` | `65536` | https://www.starlette.io/release-notes/#0180-january-23-2022 |
| PY-PV-20260522-004 | `dicttoxml` | `1.7.7 -> 1.7.8` | Boolean XML text under `dicttoxml(..., attr_type=False, root=False)` | `<ok>True</ok><no>False</no>` | `<ok>true</ok><no>false</no>` | https://raw.githubusercontent.com/quandyfactory/dicttoxml/master/README.md |
| PY-PV-20260522-005 | `sanic` | `23.3.0 -> 23.6.0` | `Sanic("probe").config.KEEP_ALIVE_TIMEOUT` | `5` | `120` | https://sanic.readthedocs.io/en/latest/sanic/changelog.html |
| PY-PV-20260522-006 | `sismic` | `0.26.8 -> 0.26.9` | `export_to_yaml` on a tiny statechart, with `ruamel.yaml==0.17.21` | quoted keys and string values | unquoted YAML keys and values | https://sismic.readthedocs.io/en/1.6.7/changelog.html |
| PY-PV-20260522-007 | `click` | `8.2.2 -> 8.3.0` | `@click.option(flag_value="upper", default=True)` under `CliRunner` | callback value `"True"` as string | callback value `"upper"` | https://click.palletsprojects.com/en/stable/changes/#version-8-3-0 |
| PY-PV-20260522-008 | `babel` | `2.13.1 -> 2.14.0` | `Locale.parse("en").number_symbols` layout | top-level `decimal` is `"."` | top-level `decimal` is null; `latn.decimal` is `"."` | https://babel.pocoo.org/en/stable/changelog.html#version-2-14-0 |
| PY-PV-20260522-009 | `multidict` | `6.2.0 -> 6.3.0` | `MultiDict([("a", "1"), ("b", "2")]).popitem()` | returns `("a", "1")` | returns `("b", "2")` | https://multidict.aio-libs.org/en/stable/changes/ |
| PY-PV-20260522-010 | `python-json-logger` | `3.0.1 -> 3.1.0` | `JsonFormatter("%(message)s %(payload)s")` with `extra={"payload": b"abc"}` | payload `"b'abc'"` | payload `"YWJj"` | https://nhairs.github.io/python-json-logger/latest/changelog/ |
| PY-PV-20260522-011 | `pygments` | `2.8.1 -> 2.9.0` | `highlight(..., HtmlFormatter(linenos="table", filename="demo.py"))` | filename span inside code cell | filename in separate table header row | https://pygments.org/docs/changelog/#version-2-9-0 |
| PY-PV-20260522-012 | `markdown` | `3.8.2 -> 3.9.0` | Footnotes extension with references in a different order than definitions | footnote order `["a", "b"]` | footnote order `["b", "a"]` | https://python-markdown.github.io/changelog/ |
| PY-PV-20260522-013 | `loguru` | `0.5.3 -> 0.6.0` | `logger.add(..., serialize=True)` with message `"\u96ea"` | JSON contains `\u96ea` escape | JSON contains literal character | https://loguru.readthedocs.io/en/latest/project/changelog.html |
| PY-PV-20260522-014 | `yarl` | `1.9.9 -> 1.9.10` | `URL("https://web.archive.org/web/").join(URL("./https://github.com/aio-libs/yarl"))` | `.../https:/github.com/...` | `.../https://github.com/...` | https://yarl.aio-libs.org/en/stable/changes/ |

## No-diff Or Inconclusive Probes

| Package | Versions | Probe result | Note |
| --- | --- | --- | --- |
| `multidict` | `5.2.0 -> 6.0.0` | no diff | Wrong version window; corrected to `6.2.0 -> 6.3.0`. |
| `python-dotenv` | `0.17.1 -> 0.18.0` | no diff | `set_key(..., quote_mode="auto")` wrote `TOKEN=abc123` in both versions for the tested fixture. |
| `jsonpickle` | `1.4.2 -> 1.5.0` | no diff | Repeated dict under `make_refs=False, unpicklable=False` serialized identically for the tested fixture. |
| `sqlparse` | `0.5.0 -> 0.5.1` | no diff | `format("select 1 -- note\nfrom t", strip_comments=True)` returned the same text for the tested fixture. |
| `requests` | `2.25.0 -> 2.25.1` | no diff | The hand-built JSON `Response` fixture used in this run produced identical decoded text. |
| `loguru` | `0.5.3 -> 0.6.0` | first attempt inconclusive | Initial probe printed raw non-ASCII through the Windows console and hit encoding noise; rerun with a Unicode escape literal passed. |

## Batch Discipline

- Batch 1: `jinja2`, `werkzeug`, `starlette`, `dicttoxml`; accepted 4/4.
- Batch 2: `sanic`, `sismic`, `click`, `babel`; accepted 4/4.
- Batch 3: `multidict` wrong window, `python-dotenv`, `jsonpickle`, `sqlparse`; accepted 0/4.
- Batch 4: corrected `multidict`, `python-json-logger`, `pygments`, `loguru`; accepted 3/4, with `loguru` rerun needed for encoding-safe output.
- Batch 5: `yarl`, `markdown`, `requests`, `loguru` rerun; accepted 3/4.

## Promotion Notes

- Promote first: `jinja2`, `werkzeug`, `starlette`, `dicttoxml`, `sanic`,
  `sismic`, `babel`, `python-json-logger`, `pygments`, `markdown`, `loguru`,
  and `yarl`.
- Treat `click` and `multidict` as useful evidence but policy-sensitive because
  the reproducing intermediate versions are yanked.
- `sismic` needs explicit dependency pin `ruamel.yaml==0.17.21`.
- `dicttoxml` should use Python 3.9 or an explicit compatibility workaround for
  old imports on newer Python.
