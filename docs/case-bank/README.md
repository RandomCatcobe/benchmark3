# SilentDrift Case Bank

This directory is the canonical case-bank layout described in
`docs/case-bank-restructure/final-plan.md`.

Each case lives under `cases/<primary-scenario>/<case-id-slug>/` and contains
public task files, a minimal probe client, metadata, and hidden oracle material.
Public evaluation packaging strips every `hidden/` directory without parsing
file contents.

## Current Status (new, 2026-05-22)

- Total packages: 103.
- Narrow ship set: 46 `verified_keep` packages.
- Wider review set: 53 packages, counting `verified_keep` plus
  `rejected_no_diff` controls.
- OLD15 replay packages: 15 total, with 12 `verified_keep`,
  2 `rejected_no_diff`, and 1 `blocked_runtime`.

| Status | Count | Package role |
| --- | ---: | --- |
| `verified_keep` | 46 | directly shippable positive silent-drift cases |
| `rejected_no_diff` | 7 | no-diff controls or audit records |
| `blocked_runtime` | 15 | runtime blocked |
| `blocked_dependency` | 27 | dependency blocked |
| `needs_source` | 8 | source evidence not strong enough yet |

## Lifecycle

![SilentDrift case lifecycle](assets/silentdrift-state-machine.svg)

The state machine is intentionally plain: a candidate becomes a direct ship
package only when old and new versions both run, and the observed behavior
changes.

## Ledgers

- `migration-30-50-ledger.md` tracks the 2026-05-21 sequential 30 and reverse
  50 verification migrations.
- `old-15-replay-ledger.md` tracks the 2026-05-22 OLD15 replay migration.
- `indexes/` contains generated metadata views and should be regenerated after
  any `metadata.json` change.

## Commands

Validate the case-bank:

```bash
python -m case_bank validate --cases docs/case-bank/cases/
```

Regenerate indexes:

```bash
python -m case_bank index build --out docs/case-bank/indexes/
```

Build a public eval package:

```bash
python -m case_bank pack --src docs/case-bank/cases/ --out eval_package/
```

Run focused tests:

```bash
python -m pytest silent_drift_miner/tests/test_case_bank.py
```

The old compatibility workflow still exists and can write `data/curated/`,
`data/oracle/`, and `data/packages/` artifacts. The primary path for new cases
is direct case-bank source package generation:

```bash
silent-drift-miner reproduce plan --candidate-id <id> --library <library> --old-version <old> --new-version <new> --client-file <client> --out data/reproductions/<id>/spec.json
silent-drift-miner reproduce run --spec data/reproductions/<id>/spec.json --out data/reproductions/<id>
silent-drift-miner case-bank create \
  --reproduction-result data/reproductions/<id>/attempt_001/result.json \
  --candidate cases/<id>/candidate.json \
  --client cases/<id>/client.py \
  --case-id <CASE-ID> \
  --slug <case-slug> \
  --primary-scenario validation-and-policy \
  --out-root docs/case-bank/cases/
```

For already curated legacy artifacts, use:

```bash
silent-drift-miner case-bank from-curated \
  --case data/curated/<case_id>.yaml \
  --oracle data/oracle/<case_id>/oracle_spec.yaml \
  --client cases/<case_id>/client.py \
  --primary-scenario validation-and-policy \
  --out-root docs/case-bank/cases/
```

After writing a source package, validate, index, and pack. A package is not
complete until validation passes and packaging includes it.
