# Python Follow-up Search - 2026-05-23

Scope: continue from `README.md` after the holidays rebalance. The active gap is
35 additional `verified_keep` cases. This pass searched for non-holidays Python
package candidates with the same public call shape and local deterministic
behavior changes.

This file is a probe log, not a claim that the cases below are packaged. Before
promotion, each candidate still needs a case-bank folder, source wording review,
`case_bank validate`, `case_bank pack`, and tests.

## Current Baseline

- `case_bank validate`: `OK 160 case-bank packages validated`
- Current status counts from metadata:
  - `verified_keep`: 65
  - `rejected_cluster_duplicate`: 38
  - `rejected_no_diff`: 7
  - `blocked_runtime`: 15
  - `blocked_dependency`: 27
  - `needs_source`: 8

## Local Probe Passes

These version pairs were locally probed with `uv run`. All listed old/new package
versions are non-yanked on PyPI unless noted.

| Candidate | Versions | Probe result | Promotion note |
| --- | --- | --- | --- |
| `structlog` default log output gains level marker | `20.1.0 -> 20.2.0` | same `structlog.get_logger().info("hello")` call changed from no `[info]` marker to `[info     ]` marker | Strong local candidate; emit stable JSON booleans instead of raw timestamped text. |
| `packaging` prerelease `SpecifierSet.contains` behavior | `25.0 -> 26.0` | `SpecifierSet(">=1.0").contains("2.0a1")` changed from `false` to `true` | Good local candidate; needs exact changelog/source wording for the PEP 440 adaptation. |
| `rdflib` `GROUP_CONCAT` empty separator | `6.3.2 -> 7.0.0` | SPARQL `GROUP_CONCAT(?v; separator="")` changed from `"a b"` to `"ab"` | Behavior is crisp; review major-version context before strict keep. |
| `odfdo` paragraph whitespace formatting | `3.7.7 -> 3.8.0` | `Paragraph("a  b\nc\td").serialize()` changed from literal whitespace to ODF `<text:s>`, `<text:line-break/>`, and `<text:tab/>` tags | Strong local candidate; uncommon package but deterministic and minor release. |
| `lxml` removed-node tail retention | `4.4.3 -> 4.5.0` | deleting `<a/>tail` from `<root><a/>tail<b/></root>` changed removed-node serialization from `<a/>` to `<a/>tail` | Strong local candidate; used Python 3.8 because old wheels are friendlier there. |
| `pytest` default short summary | `5.3.5 -> 5.4.0` | wrapping `pytest.main([failing_test, "-q"])` changed `has_short` from `false` to `true` | Candidate is tool-output behavior; wrapper exits 0 while pytest's returned code stays 1. |
| `mypy` default cache side effects | `1.19.0 -> 2.0.0` | default cache changed from JSON files to SQLite DB presence | Local and deterministic; review whether cache side effects are acceptable benchmark output. |
| `pathspec` gitwildmatch descendants | `0.9.0 -> 0.10.1` | `PathSpec.from_lines("gitwildmatch", ["dir/*"]).match_file("dir/sub/a.txt")` changed from `false` to `true` | Use `0.10.1`, not yanked `0.10.0`; source note is attached to `0.10.0` major changes. |
| `rich` empty `NO_COLOR` handling | `13.9.4 -> 14.0.0` | empty `NO_COLOR` changed `Console(...).print("[red]x[/red]")` from no ANSI to ANSI output | Borderline because the release text drove a major bump. |
| `docutils` HTML5 footnote wrapper | `0.18.1 -> 0.19` | HTML5 body gained outer `<aside class="footnote-list ...">` wrapper | Already a hold candidate; deterministic but source frames it as output change. |

## Probe Failures Or Non-Promotions

| Candidate | Versions | Result |
| --- | --- | --- |
| `dateparser` locale memory | `1.0.0 -> 1.1.0` | Needed `regex==2021.11.10` to avoid runtime regex incompatibility, then tested fixture produced no diff. |
| `Pillow` resize default | `6.2.2 -> 7.0.0` | Both old and new failed to build on local Windows/Python 3.9 because old Pillow needed source build dependencies such as zlib. |
| `python-dotenv` `set_key(..., quote_mode="auto")` | `0.17.1 -> 0.18.0` | Tested alphanumeric fixture produced identical `TOKEN=abc123`. |
| `sqlparse` `strip_comments=True` | `0.5.0 -> 0.5.1` | Tested fixture produced identical `select 1\nfrom t`. |
| `black` 2024 stable style | `23.12.1 -> 24.1.0` | Tested Unicode-escape fixture produced identical formatting. Needs a better source-backed fixture if retried. |
| `ruff` default target version | `0.7.4 -> 0.8.0` | `python -m ruff` failed inside the transient `uv run` environment because the package wrapper could not locate `ruff.exe`; do not count from this probe. |
| `click` flag default | `8.2.1 -> 8.3.0` | Non-yanked `8.2.1` already returned `"upper"`; the known differing `8.2.2` version is yanked, so do not count it. |
| `markdown` footnote reference order | `3.8.2 -> 3.9` | Simple position probe found no diff. Existing note says this is transient and needs a better fixture. |

## Suggested Next Packaging Order

1. `odfdo`
2. `lxml`
3. `structlog`
4. `packaging`
5. `pytest`
6. `mypy`
7. `rdflib`
8. `pathspec`

Keep `rich` and `docutils` as lower-tier candidates unless the strict policy
allows major/output-change release notes. Avoid `holidays` entirely for the next
batch.
