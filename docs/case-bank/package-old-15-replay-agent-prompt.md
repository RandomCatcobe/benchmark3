# Agent Prompt: Replay Old 15 Cases Into New Case Bank

You are working in `shishan/worktree/beachmark4silentdrift`.

Your job is to prepare, replay, and migrate the legacy records under `cases/`
for exactly the 15 old cases listed below. First prepare the run plan and
verify the current tooling is ready, then run the old/new replays, then move
the replay results into the new case-bank layout under `docs/case-bank/cases/`.

Do not migrate, edit, delete, or re-run any other case. Do not treat old
README claims as sufficient proof. Reproduce from the old records again.

## Current Tooling Preconditions

Before starting the 15-case replay, confirm the direct case-bank writer bridge
is present and safe to use:

```powershell
python -m pytest silent_drift_miner/tests/test_case_bank.py silent_drift_miner/tests/test_case_bank_writer.py -q
python -m case_bank validate --cases docs/case-bank/cases/
```

The writer must reject unsafe slug path traversal, refuse verified cases whose
only observed stdout change is version metadata, validate `from-curated` oracle
identity, and strip public client dependency/cache artifacts such as `.gradle/`,
`node_modules/`, `.venv/`, `vendor/`, `bin/`, `obj/`, `target/`, build output,
compiled files, and transient logs. If these checks are failing, stop and fix
the bridge before running old-15 migration work.

## Scope

Only these legacy case folders are in scope:

1. `cases/dotnet_toy_drift`
2. `cases/go_toy_drift`
3. `cases/httpx_json_request_body_compact`
4. `cases/js_toy_drift`
5. `cases/jvm_toy_drift`
6. `cases/numpy_choice_shuffle_with_p`
7. `cases/pandas_read_csv_uint8_overflow`
8. `cases/pandas_str_replace_regex_default`
9. `cases/pandas_timestamp_to_datetime64_resolution`
10. `cases/php_toy_drift`
11. `cases/polars_cast_strict_float_to_int`
12. `cases/pydantic_field_alias_none`
13. `cases/pydantic_optional_field_required`
14. `cases/ruby_toy_drift`
15. `cases/sklearn_kmeans_n_init_auto`

Everything else in `docs/case-bank/cases/`, `docs/verification-runs/`,
`online/`, and other idea-bank docs is out of scope except when used as a
format reference.

## Source Records

For each case, use the old package record as the source of truth:

- `cases/<old_case>/candidate.json`
- `cases/<old_case>/README.md`
- `cases/<old_case>/client*` or `cases/<old_case>/client/`
- local `old/` and `new/` package roots when present
- historical Python oracle/curation material under `data/curated/` and
  `data/oracle/` when present

If a `candidate.json` has `reproduction_command`, use it as the first guide,
but do not blindly trust stale paths. If no command exists, reconstruct the
plan from the old record fields and current adapter CLI.

## Required Replay

For every scoped case:

1. Prepare a short per-case run note before executing anything: ecosystem,
   likely adapter, old/new versions, client path, expected command shape, and
   known local package/source roots.
2. Read the old record and identify ecosystem, library, old/new versions,
   client path, API surface, source URL, and expected old/new observation if
   present.
3. Create or refresh a replay spec under `data/verification/old_15/<slug>/`.
4. Run a fresh old/new replay using the current pipeline or adapter.
5. Record the raw replay result under `data/verification/old_15/<slug>/`.
6. Decide status from the fresh replay, not from old docs:
   - `verified_keep`: old and new both run successfully and observable behavior differs.
   - `rejected_no_diff`: replay succeeds but no relevant behavior diff remains.
   - `blocked_dependency`: package/runtime/tool acquisition blocks the replay.
   - `blocked_runtime`: the replay starts but runtime/tool execution fails.
   - `needs_source`: source evidence is insufficient or stale and must be rechecked.
7. Create a new case-bank folder for every one of the 15 records, even blocked
   or rejected ones. The case-bank must represent the replay outcome, not only
   successful silent drift.

## New Package Contract

Each output case must live at:

```text
docs/case-bank/cases/<primary-scenario>/<slug>/
```

Each output folder must contain at minimum:

```text
case.md
evidence.md
env.md
metadata.json
client/
```

For `verified_keep` cases only, also include:

```text
hidden/oracle.md
hidden/expected.json
```

Use the current contract documents:

- `docs/case-bank/README.md`
- `docs/case-bank-restructure/final-plan.md`
- `docs/case-bank-restructure/case-folder-contract.md`
- `docs/case-bank-restructure/tag-taxonomy.md`

Do not copy dependency caches, virtual environments, `node_modules`, `vendor`,
`bin`, `obj`, jars, generated build output, or old `__pycache__` files into the
new package.

## Identity And Slugs

Prefer stable case IDs that clearly mark this as an old-15 replay. A practical
pattern is:

```text
OLD15-001 ... OLD15-015
```

Keep the old case folder name in:

- `metadata.json.provenance.old_case_path`
- `metadata.json.provenance.old_case_id`
- `evidence.md`
- the replay ledger

Use lowercase kebab-case slugs derived from the old folder names, for example:

```text
old15-pandas-str-replace-regex-default
```

Before writing a package, search existing `docs/case-bank/cases/**/metadata.json`
for the same old case path or case ID. If an exact old-15 replay package already
exists, update that package. If a semantically similar package exists from a
different source, do not overwrite it; create the old-15 replay package and
cross-reference the existing package in `evidence.md`.

Use the direct writer bridge when the replay artifacts are suitable:

```powershell
silent-drift-miner case-bank create `
  --reproduction-result data/verification/old_15/<slug>/attempt_001/result.json `
  --candidate cases/<old_case>/candidate.json `
  --client cases/<old_case>/<client-entry> `
  --case-id OLD15-### `
  --slug old15-<old-case-slug> `
  --primary-scenario <scenario> `
  --out-root docs/case-bank/cases/
```

Use `case-bank from-curated` only when a real curated case and matching
`oracle_spec.yaml` exist. The oracle `case_id` and `candidate_id` must match the
curated case; do not pass placeholder oracle specs just to satisfy the command.

## Replay Notes By Case

- `dotnet_toy_drift`: use the .NET adapter and local old/new roots from the
  legacy folder.
- `go_toy_drift`: use the Go adapter and local old/new roots from the legacy
  folder.
- `httpx_json_request_body_compact`: Python package replay; check existing
  `data/curated/httpx_json_request_body_compact/` and
  `data/oracle/httpx_json_request_body_compact/`.
- `js_toy_drift`: use the JS adapter and local old/new roots from the legacy
  folder.
- `jvm_toy_drift`: use the JVM adapter and local old/new source roots from the
  legacy folder.
- `numpy_choice_shuffle_with_p`: old docs say this was previously dropped as
  no diff after metadata filtering. Re-run and record the fresh result.
- `pandas_read_csv_uint8_overflow`: Python package replay; historical oracle
  material exists under `data/oracle/`.
- `pandas_str_replace_regex_default`: Python package replay; old record uses
  Python 3.10 and `numpy==1.24.4` stabilizer.
- `pandas_timestamp_to_datetime64_resolution`: Python package replay;
  historical oracle material exists under `data/oracle/`.
- `php_toy_drift`: use the PHP adapter and local old/new roots from the legacy
  folder.
- `polars_cast_strict_float_to_int`: old docs say this was previously dropped
  as no diff after metadata filtering. Re-run and record the fresh result.
- `pydantic_field_alias_none`: Python package replay; historical oracle
  material exists under `data/oracle/`.
- `pydantic_optional_field_required`: Python package replay; historical oracle
  material exists under `data/oracle/`.
- `ruby_toy_drift`: use the Ruby adapter and local old/new roots from the
  legacy folder.
- `sklearn_kmeans_n_init_auto`: Python package replay; historical oracle
  material exists under `data/oracle/`.

## Ledger

Create or update:

```text
docs/case-bank/old-15-replay-ledger.md
```

The ledger must include one row per old case:

```text
old_case | new_case_id | new_case_path | replay_result_path | status | notes
```

Include blocked reason and first failing step for every blocked case.

## Validation Before Handoff

After all 15 packages are written, run:

```powershell
python -m case_bank validate --cases docs/case-bank/cases/
python -m case_bank index build --out docs/case-bank/indexes/
python -m case_bank pack --src docs/case-bank/cases/ --out eval_package_old15_check/
python -m pytest silent_drift_miner/tests/test_case_bank.py
```

If packaging creates `eval_package_old15_check/`, do not commit that generated
package unless the user explicitly asks. It is only a local validation artifact.

## Handoff

Stop after the old-15 replay migration and validation. Report:

- how many of the 15 became `verified_keep`
- how many became `rejected_no_diff`
- how many became each blocked status
- the ledger path
- every new package path
- any command that failed and the exact first blocker

Do not push unless the user explicitly asks.
