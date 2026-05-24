# SilentDrift Case Bank

This directory is the canonical case-bank layout described in
`docs/case-bank-restructure/final-plan.md`.

Each case lives under `cases/<primary-scenario>/<case-id-slug>/` and contains
public task files, a minimal probe client, metadata, and hidden oracle material.
Public evaluation packaging strips every `hidden/` directory without parsing
file contents.

## Current Status (2026-05-24)

- Total packages: 196.
- Narrow ship set: 101 `verified_keep` packages.
- The original 46 approved `verified_keep` packages remain counted but were not
  rerun during the 2026-05-24 strict expansion.
- The 2026-05-24 expansion added 36 `verified_keep` packages across Python,
  JavaScript, JVM, Go, and Ruby. Data-table families such as holidays,
  time-zone, phone-number, and public-suffix updates are intentionally capped so
  they do not dominate the keep set.
- OLD15 replay packages: 15 total, with 12 `verified_keep`,
  2 `rejected_no_diff`, and 1 `blocked_runtime`.

| Status | Count | Package role |
| --- | ---: | --- |
| `verified_keep` | 101 | directly shippable positive silent-drift cases |
| `rejected_no_diff` | 7 | no-diff controls or audit records |
| `blocked_runtime` | 15 | runtime blocked |
| `blocked_dependency` | 27 | dependency blocked |
| `needs_source` | 8 | source evidence not strong enough yet |
| `rejected_cluster_duplicate` | 38 | clean reproductions rejected to avoid over-weighting one source cluster |

## 2026-05-24 Handoff

The strict expansion stop line is `101` `verified_keep` packages. The last
accepted batch deliberately stops just above the 100-package target instead of
adding every clean data-table candidate found by agents.

Verification completed before handoff:

```bash
python -m case_bank validate --cases docs/case-bank/cases
python -m case_bank index build --out docs/case-bank/indexes
python -m case_bank pack --src docs/case-bank/cases --out fresh-eval-package-101
python -m pytest silent_drift_miner/tests -q -p no:cacheprovider
```

The local pack directory is reproducible output and is not part of the source
case-bank. Rebuild it with the command above when a fresh eval bundle is needed.

Do not expand the keep set with more `holidays`, public-suffix, phone-number,
or time-zone rows just to raise the count; those clusters already have enough
representation for this pass. If a future pass needs more non-cluster material,
the best unpromoted leads from the final search round were:

- Go: `github.com/mitchellh/mapstructure` `1.4.3 -> 1.5.0`,
  `github.com/alecthomas/chroma/v2` `2.23.1 -> 2.24.0`,
  `github.com/rivo/uniseg` `0.4.6 -> 0.4.7`.
- JVM: `commons-lang3` `3.12.0 -> 3.13.0`, `commons-codec`
  `1.16.1 -> 1.17.0`, `commons-compress` `1.27.1 -> 1.28.0`.
- Reject or treat as low-priority: Ruby `holidays` and `tzinfo-data` additions,
  JS/Ruby/Java phone-number and public-suffix duplicates, and security-fix-only
  sanitizer URL cases unless the benchmark policy explicitly allows that track.

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

Build a SilentDriftBench scorer-ready eval pack:

```bash
python -m case_bank eval-pack --src docs/case-bank/cases/ --out chanwu_eval_pack/
```

The eval pack defaults to `verified_keep` only. `rejected_no_diff` controls are
included only when named explicitly with `--hard-negative-case <case_id>` or a
deliberate `--hard-negative-limit`; blocked and source-needed records stay out.
The generated manifest records the provided source path, not a fixed machine
path.

Run focused tests:

```bash
python -m pytest silent_drift_miner/tests -q -p no:cacheprovider
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
