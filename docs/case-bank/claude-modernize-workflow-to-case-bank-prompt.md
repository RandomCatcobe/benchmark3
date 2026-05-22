# Claude Prompt: Make The Pipeline Produce New Case-Bank Artifacts Directly

You are working in `shishan/worktree/beachmark4silentdrift`.

Your task is to change the old SilentDrift workflow so its primary output is the
new case-bank layout from the beginning, instead of producing old-style
`data/packages/` artifacts that later need manual migration.

Do not migrate a new batch of cases as part of this task. This task is pipeline
modernization only.

## Current Situation

The repository currently has two partially separate paths:

1. Old workflow:
   - `silent-drift-miner mine`
   - `silent-drift-miner triage ...`
   - `silent-drift-miner reproduce plan/run/summarize`
   - `silent-drift-miner curate create`
   - `silent-drift-miner oracle generate/validate`
   - `silent-drift-miner bench package`
   - `silent-drift-miner audit case`

   This path writes old-style artifacts under:

   ```text
   data/reproductions/
   data/curated/
   data/oracle/
   data/packages/
   data/audit/
   ```

2. New case-bank path:
   - canonical source packages live under `docs/case-bank/cases/**`
   - `python -m case_bank validate`
   - `python -m case_bank index build`
   - `python -m case_bank pack`

   This path can validate, index, and pack existing new case-bank folders, but
   it does not yet receive artifacts directly from the old workflow.

The missing piece is the bridge from a reproduction/curation/oracle result into:

```text
docs/case-bank/cases/<primary-scenario>/<slug>/
  case.md
  evidence.md
  env.md
  metadata.json
  client/
  hidden/
    oracle.md
    expected.json
```

## Goal

Make the normal workflow produce new case-bank source packages directly.

After your change, an operator should be able to run a documented sequence from
candidate/reproduction inputs and end with a complete, validated case-bank
folder under `docs/case-bank/cases/**`, ready for:

```powershell
python -m case_bank validate --cases docs/case-bank/cases/
python -m case_bank index build --out docs/case-bank/indexes/
python -m case_bank pack --src docs/case-bank/cases/ --out eval_package/
```

The operator should not have to hand-write `case.md`, `evidence.md`, `env.md`,
`metadata.json`, `hidden/oracle.md`, or `hidden/expected.json` for ordinary
cases.

## Non-Goals

- Do not delete the old workflow yet.
- Do not remove `data/reproductions/`, `data/curated/`, `data/oracle/`, or
  `data/packages/` compatibility paths unless tests prove no callers need them.
- Do not rewrite unrelated mining, triage, adapter, or documentation systems.
- Do not migrate the old 15 cases, 30+50 cases, online cases, or any other new
  batch as part of this task.
- Do not introduce live network or live LLM requirements into tests.

## Required Design

Implement a clear code path that converts current workflow artifacts into a new
case-bank source package.

Prefer a CLI shape like one of these:

```powershell
silent-drift-miner case-bank create `
  --reproduction-result data/verification/example/attempt_001/result.json `
  --candidate cases/example/candidate.json `
  --client cases/example/client.py `
  --source-url https://example.invalid/release-notes `
  --source-excerpt "..." `
  --retrieved-at 2026-05-22 `
  --case-id EXAMPLE-001 `
  --slug example-case `
  --primary-scenario parsing-and-ingestion `
  --out-root docs/case-bank/cases/
```

or:

```powershell
silent-drift-miner case-bank from-curated `
  --case data/curated/example.yaml `
  --oracle data/oracle/example/oracle_spec.yaml `
  --client cases/example/client.py `
  --primary-scenario parsing-and-ingestion `
  --out-root docs/case-bank/cases/
```

Choose the exact CLI that best fits the existing code, but make it obvious,
tested, and documented.

## Required Output Rules

For every generated case-bank package:

1. `metadata.json` must pass the current `case_bank.schema.validate_metadata`
   rules.
2. `case.md` must describe the task and public behavior without leaking hidden
   oracle assertions.
3. `evidence.md` must include source URL, source excerpt or provenance note,
   old/new versions, replay/reproduction result path, and review notes.
4. `env.md` must include exact local command shape or reproduction environment
   notes sufficient for another agent to rerun.
5. `client/` must contain only public client/probe material needed by the
   evaluator.
6. For `verified_keep`, `hidden/oracle.md` and `hidden/expected.json` must be
   generated.
7. For `rejected_no_diff`, `blocked_dependency`, `blocked_runtime`, and
   `needs_source`, do not create fake hidden oracle assertions. Still generate
   public package files and metadata with the correct status and provenance.
8. Generated packages must never include dependency caches, virtual
   environments, `node_modules`, `vendor`, `.venv`, `__pycache__`, compiled
   bytecode, `bin`, `obj`, jars, or transient build output.

## Status Mapping

Map old workflow outcomes into new case-bank statuses:

- reproduction keep true and meaningful old/new behavior diff:
  `verified_keep`
- run succeeds but no meaningful behavior diff:
  `rejected_no_diff`
- missing dependency, package acquisition, unavailable old runtime/toolchain:
  `blocked_dependency`
- tool exists but execution/build/runtime fails:
  `blocked_runtime`
- source evidence insufficient or not checked:
  `needs_source`

Keep first blocker details in `metadata.json.provenance` and `evidence.md`.

## Code Areas To Inspect

Read these first:

```text
silent_drift_miner/src/silent_drift_miner/cli.py
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
```

Use the current package contract as source of truth:

```text
docs/case-bank/README.md
docs/case-bank-restructure/final-plan.md
docs/case-bank-restructure/case-folder-contract.md
docs/case-bank-restructure/tag-taxonomy.md
```

## Suggested Implementation Shape

Add a small dedicated module instead of mixing this into unrelated commands.
For example:

```text
silent_drift_miner/src/silent_drift_miner/case_bank_writer.py
silent_drift_miner/src/silent_drift_miner/commands/case_bank.py
```

The writer should:

- load candidate/curated/reproduction/oracle inputs through existing structured
  loaders when available
- derive a slug and scenario
- copy or synthesize the public client into `client/`
- write Markdown files from deterministic templates
- write `metadata.json`
- write `hidden/oracle.md` and `hidden/expected.json` only for verified cases
- refuse to overwrite an existing package unless an explicit `--overwrite` flag
  is supplied
- return the created package path

Avoid fragile ad hoc string parsing when a JSON/YAML loader already exists.

## Tests Required

Add focused tests that prove the bridge works.

Minimum tests:

1. A verified Python toy reproduction result creates a valid case-bank package.
2. A `rejected_no_diff` result creates a valid package without `hidden/`.
3. A blocked result creates a valid package without fake oracle material and
   records first blocker/provenance.
4. The command refuses to overwrite by default.
5. The generated package passes `case_bank.validate_cases`.
6. `case_bank pack` strips hidden files from a generated verified package.

Use temporary fixtures. Do not rely on network, live package installs, live LLM,
or machine-specific toolchains in tests.

## Documentation Required

Update the README or docs so the current workflow is clear:

1. old compatibility path still exists
2. new primary path is direct case-bank package generation
3. exact command sequence from reproduction result to new case-bank package
4. validation/index/pack commands

If a doc is stale or conflicts with this new path, mark it historical rather
than silently relying on it.

## Acceptance Criteria

The task is complete when:

```powershell
python -m pytest silent_drift_miner/tests/test_case_bank.py
python -m pytest silent_drift_miner/tests/test_case_bank_writer.py
python -m case_bank validate --cases docs/case-bank/cases/
```

pass locally, and the new CLI can create a case-bank source package in a temp
directory from test fixtures.

Do not run a large reproduction batch. Do not migrate real packages unless the
user gives a separate instruction.

## Handoff

When finished, report:

- new command(s) added
- files changed
- tests run and results
- remaining compatibility notes
- whether old `data/packages/` is still supported
- exact command an operator should use for a normal new case
