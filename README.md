# beachmark4silentdrift

SilentDrift is a case discovery and reproduction library for silent behavioral
drift: old and new versions both run successfully, but the observable behavior
changes in a way that can silently affect callers.

This repository is the artifact factory for the benchmark. It turns leads into
reproducible, reviewable, and packageable case-bank entries.

For a plain Chinese directory map, see `duwocn.md`.

## Current Status (new, 2026-05-22)

- Total case-bank packages: 103 under `docs/case-bank/cases/**`.
- Narrow ship set: 46 `verified_keep` packages. These are the directly
  shippable positive silent-drift cases.
- Wider review set: 53 packages, counting `verified_keep` plus
  `rejected_no_diff` control packages.
- Blocked or source-check records: 50 packages, kept for audit trail and future
  promotion, not counted as directly shippable.
- OLD15 replay is included: 15 packages total, with 12 `verified_keep`,
  2 `rejected_no_diff`, and 1 `blocked_runtime`.
- Generated indexes are current under `docs/case-bank/indexes/`.

Status distribution:

| Status | Count | Meaning |
| --- | ---: | --- |
| `verified_keep` | 46 | old/new both run and behavior changes |
| `rejected_no_diff` | 7 | old/new both run but no useful behavior diff |
| `blocked_runtime` | 15 | local runtime missing or unsuitable |
| `blocked_dependency` | 27 | dependency install or resolution blocked |
| `needs_source` | 8 | needs better source evidence before promotion |

For the current handoff question:

- Strict answer: 46 packages can be sent out directly.
- Slightly wider answer: 53 packages can be reviewed as a bundle if no-diff
  controls are useful.

## Case Lifecycle

![SilentDrift case lifecycle](docs/case-bank/assets/silentdrift-state-machine.svg)

The important distinction is simple: a package is directly shippable only when
both versions execute successfully and the observed behavior changes.

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

The public files explain the task, environment, and source evidence. The
`hidden/` directory contains oracle material and expected assertions, and is
stripped when an eval package is built.

## Main Commands

Validate all case-bank folders:

```powershell
python -m case_bank validate --cases docs/case-bank/cases/
```

Build generated case-bank indexes:

```powershell
python -m case_bank index build --out docs/case-bank/indexes/
```

Build an eval package from all complete case folders:

```powershell
python -m case_bank pack --src docs/case-bank/cases/ --out eval_package/
```

Run the focused case-bank tests:

```powershell
python -m pytest silent_drift_miner/tests/test_case_bank.py
```

Run the broader test suite when touching shared tooling:

```powershell
python -m pytest
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
- `data/packages/` - older Python package-style artifacts.
- `online/` - online-only platform/API drift records.
- `silent_drift_miner/` - miner, reproduction, oracle, audit, and adapter code.

## Packaging Policy

- Do not claim a case is complete unless the folder exists, metadata validates,
  indexes regenerate, and packaging succeeds with it included.
- Do not put raw dependency caches, virtual environments, `node_modules`,
  `vendor`, `bin`, `obj`, jars, or generated build products into case folders.
- Public task files must not reveal hidden oracle conditions or exact expected
  outputs.
- Keep blocked and no-diff records when they preserve audit evidence, but do not
  count them as positive shippable silent-drift cases.
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

## 中文速读

当前 new 版 case-bank 一共有 103 个包。按最窄口径，能直接送出的正例是
46 个 `verified_keep`；按稍宽一点的口径，把 7 个 `rejected_no_diff` 对照包也放进
review 包里，一共是 53 个。OLD15 已经回放进库：15 个包里 12 个正例、2 个
no-diff、1 个 runtime blocked。
