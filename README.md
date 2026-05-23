# beachmark4silentdrift

SilentDrift is a case discovery and reproduction library for silent behavioral
drift: old and new versions both run successfully, but observable behavior
changes in a way that can silently affect callers.

This repository is the artifact factory for the benchmark. It turns leads into
reproducible, reviewable, and packageable case-bank entries.

For a plain Chinese directory map, see `duwocn.md`.

## Current Handoff Status (2026-05-23)

The strict-100 run was intentionally rebalanced after review. The earlier count
reached 103 `verified_keep`, but 38 `holidays` cases were moved out of the keep
set because they were clean reproductions from the same upstream package and
would overweight one bundled-calendar-data cluster.

Current case-bank totals:

| Status | Count | Meaning |
| --- | ---: | --- |
| `verified_keep` | 65 | positive silent-drift cases; old/new both run and behavior changes |
| `rejected_cluster_duplicate` | 38 | clean drift repros rejected because they duplicate an already represented upstream cluster |
| `rejected_no_diff` | 7 | old/new both run but no useful behavior diff |
| `blocked_runtime` | 15 | local runtime missing or unsuitable |
| `blocked_dependency` | 27 | dependency install or resolution blocked |
| `needs_source` | 8 | needs better source evidence before promotion |

Total case-bank packages: 160.

Strict keep target status:

```text
target verified_keep: 100
current verified_keep: 65
remaining gap: 35
```

The original 46 already-approved `verified_keep` cases were not rerun. They were
only read by validation, indexing, packaging, and tests.

## Latest Added Material

New Python keep material now in the case bank:

- `PY-STRICT-001`: Typer optional list `None` default.
- `PY-STRICT-002` through `PY-STRICT-017`, excluding the failed/nonexistent
  slots: Jinja2, Werkzeug, Starlette, dicttoxml, Sanic, sismic, Babel,
  python-json-logger, Pygments, Loguru, yarl, BeautifulSoup, coverage, json5,
  and filelock.
- `PY-HOL-015`, `PY-HOL-026`, `PY-HOL-036`: the only kept `holidays`
  representatives.

The remaining 38 `PY-HOL-*` cases are preserved as
`rejected_cluster_duplicate`. They are not failed replays: they have clean
old/new stdout drift, but were rejected because `PY-HOL-015`, `PY-HOL-026`, and
`PY-HOL-036` already cover value-to-null, label-normalization, and null-to-value
bundled-calendar-data drift.

## Next Handoff Task

Find at least 35 more `verified_keep` cases without leaning on the `holidays`
cluster. Prefer distinct upstream packages and API surfaces.

Recommended search order:

1. Python packages not already represented.
2. JavaScript.
3. Go.
4. JVM.
5. PHP.
6. Ruby.
7. .NET.

Gate every new candidate with the narrow criteria:

- non-yanked versions;
- no major-version jump unless the project's versioning makes that safe;
- no explicit breaking/deprecation track;
- same public API call shape on old and new;
- old/new both exit 0;
- runtime stderr is empty;
- stdout is stable JSON or otherwise stable structured output;
- behavior diff is semantic, not version banners or warning noise.

## Reproduction Helpers

The current Python batch helpers are:

- `tools/strict_python_batch.py`
- `tools/strict_python_holidays_batch.py`

`tools/strict_python_holidays_batch.py` now defaults to keeping only the three
representative `holidays` cases and marking the rest as
`rejected_cluster_duplicate`, so rerunning it with `--force` should not inflate
the keep count again.

## Case Lifecycle

![SilentDrift case lifecycle](docs/case-bank/assets/silentdrift-state-machine.svg)

A package is directly shippable only when both versions execute successfully and
the observed behavior changes.

## What Counts As Complete

A complete case-bank entry lives at:

```text
docs/case-bank/cases/<primary-scenario>/<case-id-slug>/
```

and contains:

```text
case.md
evidence.md
env.md
metadata.json
client/
hidden/
```

Only `verified_keep` entries should have `hidden/`. Rejected, blocked, and
source-needed records should keep public audit files but no hidden oracle.

## Verification Commands

Use this command shape from the repository root:

```powershell
$env:PYTHONPATH='silent_drift_miner\src'
python -m case_bank validate --cases docs\case-bank\cases
python -m case_bank index build --out docs\case-bank\indexes
python -m case_bank pack --src docs\case-bank\cases --out $env:TEMP\bench2_eval_package
python -m pytest silent_drift_miner\tests -q -p no:cacheprovider
```

Last verified after the `holidays` rebalance:

```text
case_bank validate: OK 160 case-bank packages validated
case_bank index build: OK
case_bank pack: OK
pack hidden leak check: hidden_leak_count=0
pytest: 129 passed, 1 skipped
```

## Important Paths

- `docs/case-bank/` - canonical case-bank layout, ledgers, indexes, and
  packaging prompts.
- `docs/case-bank/cases/` - complete packaged cases.
- `docs/case-bank/indexes/` - generated views over `metadata.json`.
- `docs/case-bank/migration-30-50-ledger.md` - sequential 30 and reverse 50
  migration ledger.
- `docs/case-bank/old-15-replay-ledger.md` - OLD15 replay ledger.
- `docs/case-bank-restructure/final-plan.md` - schema, folder contract, status
  meanings, and packaging rules.
- `docs/verification-runs/` - human-readable run notes for earlier verification
  passes.
- `data/verification/` - local raw replay evidence and run artifacts.
- `online/` - online-only platform/API drift records.
- `silent_drift_miner/` - miner, reproduction, oracle, audit, and adapter code.

## Packaging Policy

- Do not claim a case is complete unless the folder exists, metadata validates,
  indexes regenerate, and packaging succeeds with it included.
- Do not put raw dependency caches, virtual environments, `node_modules`,
  `vendor`, `bin`, `obj`, jars, or generated build products into case folders.
- Public task files must not reveal hidden oracle conditions or exact expected
  outputs.
- Keep blocked and rejected records when they preserve audit evidence, but do
  not count them as positive shippable silent-drift cases.
- Work with existing user or agent changes; do not revert unrelated edits.

## Local Cleanup Notes

The following are local/generated and should not be part of the shipped case
bank unless there is a specific reason:

- `eval_package*/`
- `.uv-python/`
- `.uv-cache/`
- `data/verification/**` raw replay workspaces
- Python, Node, Go, .NET, JVM, Ruby, or PHP dependency caches

## Historical Docs

The phase docs still describe how the project got here. Treat them as
historical context when they conflict with the current case-bank contract:

- `docs/phase-0-ground-rules.md`
- `docs/phase-1-pipeline-skeleton.md`
- `docs/phase-2-python-reproduction.md`
- `docs/phase-3-oracle-package-audit.md`
- `docs/phase-4-real-python-cases.md`
- `docs/phase-5-llm-client-generation.md`
- `docs/phase-6-ecosystem-expansion.md`

## 中文交接速读

当前不是 100 个可交付 keep。诚实口径是：160 个 case-bank 包里，65 个
`verified_keep`，38 个 `holidays` 聚类样本已降为
`rejected_cluster_duplicate`，还差 35 个新的、最好来自不同上游包的
`verified_keep`。

保留的 `holidays` 只有 3 个：`PY-HOL-015`、`PY-HOL-026`、`PY-HOL-036`。
其他 `holidays` 不是失败，而是同源重复度太高，不能继续帮 keep 数量冲刺。
