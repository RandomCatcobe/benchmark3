# Python Drift Run Log

Append-only batch notes for model-guided Python silent-drift discovery.

## 2026-05-19: v0.11.0 pre-run preparation

- Model/operator: Codex
- Search budget: not started
- Packages searched: none
- Ideas added: 0
- Ideas rejected: 0
- Cases promoted: 0
- Cases accepted: 0
- Notes:
  - Markdown memory helpers were implemented and pushed in `v0.11.0`.
  - Readiness and next-run brief files were generated.
  - The real discovery/search loop is intentionally still unopened.

## 2026-05-19: Python autodiscovery pilot batch 001

- Model/operator: Codex
- Search budget: 10 discovery attempts, then stop
- Packages searched: `httpx`, `jinja2`, `werkzeug`, `starlette`, `babel`, `click`, `networkx`, `attrs`, `urllib3`, `fastapi`
- Ideas added:
  - `IDEA-20260519-001`: `httpx` JSON request body compact serialization
  - `IDEA-20260519-002`: `jinja2` `groupby` default becomes case-insensitive
  - `IDEA-20260519-003`: `werkzeug.http.dump_cookie` path default transiently drops slash
  - `IDEA-20260519-004`: `starlette.responses.FileResponse` chunk size default increases
  - `IDEA-20260519-005`: `babel.core.Locale.number_symbols` gains numbering-system layer
  - `IDEA-20260519-006`: `click.option` flag default preservation changes callback value
- Ideas rejected:
  - `REJECTED-20260519-007`: NetworkX 3.0 matrix-to-array migration is too prominently announced
  - `REJECTED-20260519-008`: attrs `@define` on-setattr converters are explicit breaking change
  - `REJECTED-20260519-009`: urllib3 TLS minimum default needs network-like SSL context and is prominent
  - `REJECTED-20260519-010`: FastAPI `strict_content_type` is explicitly marked breaking
- Cases promoted: 0
- Cases accepted: 0
- Notes:
  - No code files were changed.
  - Search stayed inside Python package/library drift discovery.
  - Existing repository anchors for pandas, pydantic, scikit-learn, polars, and numpy were avoided.
  - Best next reproduction candidates are `httpx`, `jinja2`, `werkzeug`, and `click`; `babel` is borderline because the changelog says "possibly backwards incompatible".


## RUN-20260519: 2026-05-20: Python autodiscovery pilot batch 002

- Model/operator: Codex
- Search budget: 10 discovery attempts, then stop
- Packages searched:
- matplotlib
- requests
- pytest
- django
- flask
- arrow
- sqlalchemy
- pyyaml
- marshmallow
- aiohttp
- Ideas added:
- IDEA-20260520-001: matplotlib get_cmap returns a copy
- IDEA-20260520-002: requests application/json defaults to UTF-8 decoding
- IDEA-20260520-003: pytest default -r short summary reports failures/errors
- IDEA-20260520-004: Django default timezone object switches to zoneinfo
- IDEA-20260520-005: Flask session cookie domain stops using SERVER_NAME
- IDEA-20260520-006: Arrow timezone objects migrate from pytz to ZoneInfo
- Ideas rejected:
- REJECTED-20260520-007: SQLAlchemy Row containment is prominent 2.0 migration behavior
- REJECTED-20260520-008: PyYAML default loader and flow-style changes are explicit incompatibilities
- REJECTED-20260520-009: marshmallow TimeDelta float preservation is explicitly backward-incompatible
- REJECTED-20260520-010: aiohttp ClientTimeout sock_connect default is under breaking-change heading
- Cases promoted to reproduction:
- 0
- Cases accepted into benchmark:
- 0
- Notes:
- No code files were changed; search stayed inside Python package/library drift discovery.
- Avoided prior idea-bank packages plus local case anchors for pandas, pydantic, scikit-learn, numpy, and polars.
- Best next reproduction candidates: matplotlib, requests, Flask, Arrow; Django is plausible but has Python-version/setup risk; pytest needs policy review because the deterministic run returns a failing test exit code.

## RUN-20260520: Python autodiscovery pilot batch 003

- Model/operator: Codex
- Search budget: 10 discovery attempts, then stop
- Packages searched:
  - `markdown`
  - `multidict`
  - `yarl`
  - `python-json-logger`
  - `dateparser`
  - `pillow`
  - `packaging`
  - `structlog`
  - `simplejson`
  - `pymongo`
- Ideas added:
  - `IDEA-20260520-011`: Python-Markdown footnotes order by reference occurrence
  - `IDEA-20260520-012`: multidict `popitem` removes latest entry
  - `IDEA-20260520-013`: yarl `URL.join` keeps empty URL path segments
  - `IDEA-20260520-014`: python-json-logger default encodes bytes as URL-safe base64
  - `IDEA-20260520-015`: dateparser stops trying previous locales by default
  - `IDEA-20260520-016`: Pillow resize default resampling switches to BICUBIC
  - `IDEA-20260520-017`: packaging `SpecifierSet` adapts prerelease matching
  - `IDEA-20260520-018`: structlog default configuration adds log level processing
- Ideas rejected:
  - `REJECTED-20260520-019`: simplejson `allow_nan` default now raises on NaN
  - `REJECTED-20260520-020`: PyMongo JSONMode default is prominent migration-guide behavior
- Cases promoted to reproduction: 0
- Cases accepted into benchmark: 0
- Notes:
  - No code files were changed; this batch only appended Python drift discovery Markdown.
  - Avoided all previously mentioned packages and APIs from batches 001 and 002.
  - Best next reproduction candidates are `multidict`, `yarl`, `python-json-logger`, and `markdown`; `pillow` and `dateparser` need install/input-fixture checks; `packaging` needs exact PEP 440 edge input from tests or PRs.

## RUN-20260520: Python autodiscovery pilot batch 004

- Model/operator: Codex
- Search budget: 10 discovery attempts, then stop
- Packages searched:
- pygments
- sqlparse
- docutils
- mistune
- jsonpickle
- filelock
- python-dotenv
- pathspec
- celery
- cattrs
- Ideas added:
- IDEA-20260520-021: Pygments HtmlFormatter table filename row changes
- IDEA-20260520-022: sqlparse strip_comments preserves different whitespace
- IDEA-20260520-023: Docutils HTML5 footnotes move into aside
- IDEA-20260520-025: jsonpickle make_refs False serializes repeats differently
- IDEA-20260520-026: filelock logger default level stops forcing warning
- IDEA-20260520-027: python-dotenv set_key quote output changes
- IDEA-20260520-028: pathspec gitwildmatch dir star matches descendants
- Ideas rejected:
- REJECTED-20260520-024: Mistune raw HTML escaping belongs to explicit breaking change
- REJECTED-20260520-029: Celery 4.0 default serializer is prominent upgrade guidance
- REJECTED-20260520-030: cattrs sequence structuring migrations are explicit
- Cases promoted to reproduction:
- 0
- Cases accepted into benchmark:
- 0
- Notes:
- No code files were changed; this batch only appended Python drift discovery Markdown.
- Avoided all packages and APIs already mentioned in previous idea/rejection cards.
- Best next reproduction candidates are sqlparse, jsonpickle, python-dotenv, and Pygments; pathspec needs silent-policy review because the source calls it a major change.

## RUN-20260520: Python autodiscovery pilot batch 005

- Model/operator: Codex
- Search budget: 10 discovery attempts, then stop
- Packages searched:
- black
- loguru
- hypothesis
- lxml
- rdflib
- odfdo
- natsort
- bleach
- xlrd
- pyparsing
- Ideas added:
- IDEA-20260520-031: Black 2024 stable style changes formatted output
- IDEA-20260520-032: Loguru serialized JSON stops escaping non-ASCII
- IDEA-20260520-033: Hypothesis creates gitignore in example database directory
- IDEA-20260520-034: lxml addnext preserves moved tail text
- IDEA-20260520-035: RDFLib GROUP_CONCAT empty separator changes output
- IDEA-20260520-036: odfdo Paragraph formats whitespace by default
- Ideas rejected:
- REJECTED-20260520-037: natsort default numeric parsing is explicit legacy incompatibility
- REJECTED-20260520-038: Bleach sanitizer rewrites are explicit incompatible output changes
- REJECTED-20260520-039: xlrd 2.0 encoding default is buried inside major removal release
- REJECTED-20260520-040: pyparsing empty-string parse action fix is exception-path only
- Cases promoted to reproduction:
- 0
- Cases accepted into benchmark:
- 0
- Notes:
- No code files were changed; this batch only appended Python drift discovery Markdown.
- Avoided all packages and APIs already mentioned in previous idea/rejection cards plus local anchors pandas, pydantic, scikit-learn, numpy, and polars.
- Best next reproduction candidates are Loguru, Hypothesis, odfdo, and RDFLib; Black and lxml need policy/install-risk review.

## RUN-20260520: Python autodiscovery pilot batch 006

- Model/operator: Codex
- Search budget: 10 discovery attempts, then stop
- Packages searched:
  - `beautifulsoup4`
  - `fsspec`
  - `coverage`
  - `mypy`
  - `ruff`
  - `rich`
  - `json5`
  - `pyjwt`
  - `invoke`
  - `platformdirs`
- Ideas added:
  - `IDEA-20260520-041`: Beautiful Soup script `get_text` semantics change
  - `IDEA-20260520-042`: fsspec default file cache strategy changes
  - `IDEA-20260520-043`: coverage JSON report stops counting module docstrings as executed
  - `IDEA-20260520-044`: mypy default cache format switches to binary and SQLite
  - `IDEA-20260520-045`: Ruff default Python target version advances to 3.9
  - `IDEA-20260520-046`: Rich empty color environment variables no longer disable color
  - `IDEA-20260520-047`: json5 custom encoder output indentation is fixed
- Ideas rejected:
  - `REJECTED-20260520-048`: PyJWT 2.0 encode return type is too prominent
  - `REJECTED-20260520-049`: Invoke `MockContext.repeat` default is explicitly incompatible
  - `REJECTED-20260520-050`: platformdirs directory moves are labeled `BREAKING`
- Cases promoted to reproduction: 0
- Cases accepted into benchmark: 0
- Notes:
  - No code files were changed; this batch only appended Python drift discovery Markdown.
  - Avoided all previously mentioned packages/APIs plus local anchors `pandas`, `pydantic`, `scikit-learn`, `numpy`, and `polars`.
  - Best next reproduction candidates are `coverage`, `beautifulsoup4`, `json5`, and `fsspec`; `ruff`, `rich`, and `mypy` need policy review because their differences are tool defaults or side effects.

## RUN-20260519: Python autodiscovery promotion batch 001

- Model/operator: Codex
- Search budget: 1 promoted reproduction from existing IDEA card
- Packages searched:
- httpx
- Ideas added:
- None
- Ideas rejected:
- None
- Cases promoted to reproduction:
- IDEA-20260519-001 -> httpx-json-request-body-compact
- Cases accepted into benchmark:
- ACCEPTED-20260519-001: httpx_json_request_body_compact
- Notes:
- No new search; closed the markdown memory loop for the previously reproduced httpx case.
- Counts: promoted=1, accepted=1, rejected=0.
- Reproduction keep=true and package audit pass=true with no findings.

## RUN-20260522: Python self-prompt search and verification batch 007

- Model/operator: Codex
- Search budget: 10 discovery attempts, then stop
- Prompt source:
  - Agent-authored search and verification prompts recorded in `docs/python-self-prompt-run-20260522.md`.
- Packages searched:
  - `uvicorn`
  - `python-slugify`
  - `dicttoxml`
  - `python-dateutil`
  - `typer`
  - `sanic`
  - `itsdangerous`
  - `pymunk`
  - `inflection`
  - `sismic`
- Ideas added:
  - `IDEA-20260522-051`: dicttoxml boolean XML text lowercases
  - `IDEA-20260522-052`: Typer optional list default stays None
  - `IDEA-20260522-053`: Sanic keep-alive timeout default increases
  - `IDEA-20260522-054`: Sismic export_to_yaml stops quoting by default
- Ideas rejected:
  - `REJECTED-20260522-055`: Uvicorn reload_delay source did not reproduce
  - `REJECTED-20260522-056`: python-slugify regex_pattern probe found no diff
  - `REJECTED-20260522-057`: dateutil missing-day parser fix is exception-path behavior
  - `REJECTED-20260522-058`: itsdangerous SHA default change is yanked and prominent
  - `REJECTED-20260522-059`: Pymunk collection view drift is prominently breaking
  - `REJECTED-20260522-060`: inflection human pluralization was already fixed before tested boundary
- Cases promoted to reproduction: 0
- Cases accepted into benchmark: 0
- Notes:
  - No code files were changed; this batch only appended Python drift discovery Markdown and the self-prompt run brief.
  - Strongest next reproduction candidates are `dicttoxml`, `typer`, `sanic`, and `sismic`.
  - `sismic` needs a dependency pin (`ruamel.yaml==0.17.21`) to avoid unrelated old-package failure under modern dependency resolution.

## RUN-20260522: Python local verification follow-up 001

- Model/operator: Codex
- Search budget: 1 strict candidate promoted from the self-prompt batch
- Package verified:
  - `typer`
- Idea promoted:
  - `IDEA-20260522-052` -> `typer-optional-list-none-default`
- Local verification result:
  - `data\verification\python_typer_optional_list_none_default\attempt_001\result.json`
- Verdict:
  - keep=true
  - drop_reason=null
  - diff_summary=`stdout changed`
- Observed behavior:
  - old `typer==0.9.4`: callback receives `[]` with exit code 0
  - new `typer==0.10.0`: callback receives `None` with exit code 0
- Notes:
  - Used `click==8.1.7` as a shared dependency pin to avoid unrelated Click release noise.
  - `uv run --project silent_drift_miner ...` failed locally while building the editable package with `0xc0000135`; verification succeeded by running the same CLI from source with `PYTHONPATH=silent_drift_miner\src`.

## RUN-20260522: Python parallel verification batch 008

- Model/operator: Codex
- Search budget: continue searching Python silent drift and begin parallel local
  verification after each group of four candidates; stop only after at least 10
  acceptable cases.
- Detailed run sheet:
  - `docs/python-parallel-verification-run-20260522.md`
- Packages accepted by local probe:
  - `jinja2`
  - `werkzeug`
  - `starlette`
  - `dicttoxml`
  - `sanic`
  - `sismic`
  - `click`
  - `babel`
  - `multidict`
  - `python-json-logger`
  - `pygments`
  - `markdown`
  - `loguru`
  - `yarl`
- Strict non-yanked count:
  - 12 accepted probes remain after excluding `click==8.2.2` and
    `multidict==6.3.0`.
- Probes rejected or held:
  - `python-dotenv` `0.17.1 -> 0.18.0`: no diff for `set_key(..., quote_mode="auto")`.
  - `jsonpickle` `1.4.2 -> 1.5.0`: no diff for the repeated-object fixture.
  - `sqlparse` `0.5.0 -> 0.5.1`: no diff for the tested `strip_comments` fixture.
  - `requests` `2.25.0 -> 2.25.1`: no diff for the hand-built JSON response fixture.
- Notes:
  - `sismic` requires `ruamel.yaml==0.17.21`.
  - `dicttoxml` was verified on Python 3.9.
  - `loguru` needed an encoding-safe Unicode literal to avoid Windows console
    encoding noise.
  - `click` and `multidict` are real reproductions but should be separated from
    strict packaging decisions because the reproducing versions are yanked.

## RUN-20260522: Python science-pain verification batch 009

- Model/operator: Codex
- Search budget: continue Python discovery with priority on scientific
  computing, data analysis, numerical results, statistical tests, table shape,
  dtype, and visualization pain points.
- Detailed run sheet:
  - `docs/python-science-pain-verification-run-20260522.md`
- Packages accepted by local probe:
  - `pandas`
  - `numpy`
  - `scipy`
- Accepted probes:
  - `pandas.get_dummies` default dtype changes from `uint8` to `bool`.
  - `pandas.DataFrameGroupBy.apply` starts respecting `group_keys` for a transformer-like apply.
  - `pandas.to_datetime(..., errors="coerce")` mixed-format parsing can now coerce later values to null.
  - `numpy.linalg.solve` interprets stacked right-hand-side arrays differently.
  - `pandas.DataFrame.quantile` includes datetime-like columns by default.
  - NumPy default integer dtype on 64-bit Windows changes from `int32` to `int64`.
  - `numpy.gradient` returns a tuple instead of a list.
  - `numpy.any` on object arrays returns a boolean instead of one of the objects.
  - `scipy.stats.mannwhitneyu` default method changes the p-value.
  - `numpy.linalg.lstsq` default rank cutoff changes the rank and solution.
- Strict non-yanked count:
  - 10 accepted probes.
- Probes rejected or held:
  - `matplotlib` `3.6.3 -> 3.7.0`: no diff for the tested `get_cmap` mutation fixture.
  - `scikit-learn` `1.0.2 -> 1.1.3`: no diff for `r2_score` constant-target fixture after compatible pins.
  - `pandas` `1.5.3 -> 2.0.3`: no diff for the tested resample/apply fixture.
  - `pandas` `1.5.3 -> 2.0.3`: no diff for the tested `DataFrame.rank` fixture.
  - `scipy` `1.9.3 -> 1.10.1`: no diff for the tested `ttest_ind` return-object fixture.
- Notes:
  - Used `numpy==1.24.4` to stabilize pandas `1.5.3 -> 2.0.3` probes.
  - Used Python 3.9 with `numpy==1.21.6` for the SciPy `1.6.3 -> 1.7.3` probe.
  - Initial unpinned `scikit-learn` probes hit a NumPy ABI mismatch; rerun with
    `numpy==1.23.5` and `scipy==1.9.3` completed.

## RUN-20260523: Python narrow-silent direct-submit batch 010

- Model/operator: Codex
- Search budget: continue Python discovery, but count only the narrowest
  silent cases that are no-brainer direct-submit candidates.
- Detailed run sheet:
  - `docs/python-narrow-silent-verification-run-20260523.md`
- Strict direct-submit count:
  - 4 accepted probes.
- Packages accepted by local probe:
  - `beautifulsoup4`
  - `coverage`
  - `json5`
  - `filelock`
- Accepted probes:
  - `beautifulsoup4`: `script.get_text()` returns tag-local script text in
    `4.10.0` after returning an empty string in `4.9.3`.
  - `coverage`: JSON report `executed_lines` stops counting a module docstring
    in `7.13.1`.
  - `json5`: int subclasses with a custom `__str__` serialize as numeric `7`
    in `0.9.9` instead of the custom string token emitted in `0.9.8`.
  - `filelock`: importing the package no longer sets the `filelock` logger
    level in `3.3.1`, changing debug-log filtering under the same root logger.
- Verified but not counted in strict total:
  - `Flask` `2.2.5 -> 2.3.0`: session cookie domain fallback changes, but the
    release is too broad for no-brainer narrow packaging.
  - `docutils` `0.18.1 -> 0.19`: HTML5 footnote wrapper changes, but the source
    places it under output changes.
  - `arrow` `1.3.0 -> 1.4.0`: timezone implementation type changes, but the
    tested arithmetic result stayed the same.
- Probes rejected:
  - `hypothesis` `.gitignore` side effect did not reproduce.
  - `fsspec` local-file fixture bypassed the changed cache layer.
  - `json5` `0.12.0 -> 0.12.1` tested fixture found no indentation diff; use
    the verified `0.9.8 -> 0.9.9` int-subclass case instead.
