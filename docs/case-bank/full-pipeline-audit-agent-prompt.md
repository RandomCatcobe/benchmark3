# Agent Prompt: Full Pipeline Audit After Case-Bank Writer Bridge

You are working in `shishan/worktree/beachmark4silentdrift`.

Your task is to perform a full audit of the current SilentDrift pipeline after
the new direct case-bank writer bridge was added. This is an audit task, not a
new migration batch and not a broad refactor.

## Handoff Context

The pipeline now has two supported output paths:

1. Compatibility path:
   - `silent-drift-miner reproduce plan/run/summarize`
   - `silent-drift-miner curate create`
   - `silent-drift-miner oracle generate/validate`
   - `silent-drift-miner bench package`
   - `silent-drift-miner audit case`
   - output roots such as `data/reproductions/`, `data/curated/`,
     `data/oracle/`, `data/packages/`, and `data/audit/`

2. Primary new case-bank path:
   - `silent-drift-miner case-bank create`
   - `silent-drift-miner case-bank from-curated`
   - `python -m case_bank validate`
   - `python -m case_bank index build`
   - `python -m case_bank pack`
   - source packages under `docs/case-bank/cases/**`

The old compatibility path is intentionally still supported. Do not remove it
unless the user separately asks for deprecation work.

The prompt that requested the writer bridge,
`docs/case-bank/claude-modernize-workflow-to-case-bank-prompt.md`, is
intentionally retained for now. Do not delete it unless the user confirms.

## Audit Goal

Audit the complete pipeline for correctness, safety, reproducibility, and
handoff quality. Prioritize real defects and risks over style concerns.

The main question is:

Can a future operator or agent move from mined/reproduced evidence to a valid,
packable, non-leaking case-bank source package without manual hidden-oracle
leakage, stale metadata, or broken compatibility behavior?

## Files To Read First

Read these before forming conclusions:

```text
silent_drift_miner/src/silent_drift_miner/cli.py
silent_drift_miner/src/silent_drift_miner/case_bank_writer.py
silent_drift_miner/src/silent_drift_miner/commands/case_bank.py
silent_drift_miner/src/silent_drift_miner/commands/reproduce.py
silent_drift_miner/src/silent_drift_miner/commands/curate.py
silent_drift_miner/src/silent_drift_miner/commands/oracle.py
silent_drift_miner/src/silent_drift_miner/commands/bench.py
silent_drift_miner/src/silent_drift_miner/reproduction.py
silent_drift_miner/src/silent_drift_miner/curation.py
silent_drift_miner/src/silent_drift_miner/oracle.py
silent_drift_miner/src/silent_drift_miner/bench.py
silent_drift_miner/src/case_bank/schema.py
silent_drift_miner/src/case_bank/validation.py
silent_drift_miner/src/case_bank/index.py
silent_drift_miner/tests/test_case_bank.py
silent_drift_miner/tests/test_case_bank_writer.py
docs/case-bank/README.md
docs/case-bank-restructure/final-plan.md
docs/case-bank-restructure/case-folder-contract.md
docs/case-bank-restructure/tag-taxonomy.md
```

Also sample a few existing packages under `docs/case-bank/cases/**` and compare
their structure against writer-generated packages in tests.

## Audit Areas

Check at least these areas:

- CLI ergonomics: required flags, failure messages, overwrite behavior, and
  whether `artifact-root` restrictions are preserved.
- Status mapping: `verified_keep`, `rejected_no_diff`, `blocked_dependency`,
  `blocked_runtime`, and `needs_source`.
- Metadata correctness: schema compliance, scenario values, drift pattern and
  failure mode defaults, provenance fields, source URLs, and old/new versions.
- Hidden material: verified cases must get hidden oracle material; non-verified
  cases must not get fake `hidden/expected.json`.
- Public package safety: copied clients must not include caches, virtualenvs,
  `node_modules`, `vendor`, build outputs, compiled files, jars, or transient
  logs.
- Oracle assertions: generated `expected.json` must be meaningful enough for
  verified cases and must not silently assert on version metadata only.
- Path handling: relative/absolute inputs, Windows paths, path traversal,
  existing package overwrite protection, and output root behavior.
- Compatibility path: old `curate`, `oracle`, `bench package`, and `audit`
  commands should still work.
- Documentation: current docs should explain the new primary path without
  making old historical docs actively misleading.
- Tests: coverage should include both writer behavior and cross-command
  compatibility; identify important missing cases.

## Mechanical Verification

Run these commands locally:

```powershell
python -m pytest silent_drift_miner/tests/test_case_bank.py silent_drift_miner/tests/test_case_bank_writer.py -q
python -m case_bank validate --cases docs/case-bank/cases/
python -m pytest silent_drift_miner/tests -q -p no:cacheprovider
```

If a command fails, capture the exact command, failure mode, and whether it is a
new regression or an environmental issue.

Do not run live network, live LLM, or large package migration batches.

## Suggested Extra Probes

Use temporary directories only. Good probes include:

- Create a verified writer package from a JSON stdout diff where only a version
  metadata field changes; confirm it is not accepted as a meaningful assertion.
- Create a client directory containing excluded subdirectories such as
  `node_modules`, `.venv`, `__pycache__`, `vendor`, `bin`, `obj`, and confirm
  the generated package strips them.
- Create blocked runtime and blocked dependency fixtures and verify their
  metadata/provenance differs correctly.
- Exercise `case-bank from-curated` with relative reproduction paths.
- Confirm `case_bank pack` strips hidden material from a writer-generated
  verified package.

## Output Contract

Return findings first, ordered by severity. For each finding include:

- severity (`P0`, `P1`, `P2`, or `P3`)
- file and line reference
- why it matters
- a minimal reproduction or reasoning path
- suggested fix

Then include:

- commands run and results
- test gaps or residual risk
- compatibility notes for old `data/packages/`
- whether the writer bridge is safe to use for the next real case

If there are no findings, say that clearly and list remaining risks.

## Boundaries

Do not migrate the old 15 cases, the 30+50 verification cases, online cases, or
any new batch.

Do not delete `docs/case-bank/claude-modernize-workflow-to-case-bank-prompt.md`
without explicit user confirmation.

Do not push, tag, or publish anything unless the user specifically asks.
