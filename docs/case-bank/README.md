# SilentDrift Case Bank

This directory is the self-contained case-bank layout described in `docs/case-bank-restructure/final-plan.md`.

Each case lives under `cases/<primary-scenario>/<case-id-slug>/` and contains public task files, a minimal probe client, and hidden oracle material.

Public evaluation packaging strips every `hidden/` directory without parsing file contents.

The 2026-05-21 `sequential_30` and `reverse_50` verification runs are tracked in `migration-30-50-ledger.md`. That ledger includes successful silent-drift cases and unsuccessful blocked/rejected records.

## Commands

The old compatibility workflow still exists and can write `data/curated/`,
`data/oracle/`, and `data/packages/` artifacts. The primary path for new cases is
now direct case-bank source package generation:

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

After writing a source package, validate, index, and pack:

```bash
python -m case_bank index build --out docs/case-bank/indexes/
python -m case_bank validate --cases docs/case-bank/cases/
python -m case_bank pack --src docs/case-bank/cases/ --out eval_package/
```

The generated indexes are views over `metadata.json` files and should be regenerated after any case metadata change.
Run validation before packaging or migrating new completed cases; it checks metadata, public files, client folders, and hidden expected assertions for verified cases.
