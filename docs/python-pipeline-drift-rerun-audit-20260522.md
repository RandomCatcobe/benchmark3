# Python Pipeline Drift Rerun Audit - 2026-05-22

This audit reran the 10 cases from
`docs/python-pipeline-drift-verification-run-20260522.md` after the user asked
whether they were directly usable and whether any result was hallucinated.

## Verdict

- Behavior rerun: 10/10 passed.
- Hallucination check: no hallucinated behavior found. Every old/new pair
  reproduced the recorded stdout-level difference.
- Direct packaging check: 10/10 can be turned into package candidates with the
  recorded version and dependency pins.
- Strict silent-policy check: policy-sensitive. Several cases are high-quality
  pipeline/schema drift, but are documented in prominent pandas 3.0, pandas 2.0,
  Polars 0.20, or Dask 2023.7.1 upgrade notes. Keep quality and strict
  quietness as separate labels.

## Rerun Results

| Case | Rerun old output | Rerun new output | Behavior verdict | Packaging note |
| --- | --- | --- | --- | --- |
| pandas Index narrow dtype | `pandas=1.5.3`, `dtype=int64` | `pandas=2.0.3`, `dtype=int8` | pass | Direct with `numpy==1.24.4`; policy-sensitive because pandas 2.0 notes document dtype preservation. |
| Polars value_counts schema | `polars=0.19.19`, columns `["cat", "counts"]` | `polars=0.20.0`, columns `["cat", "count"]` | pass | Direct; schema-output drift. |
| Polars Expr.count null semantics | group `a` count `2` | group `a` count `1` | pass | Direct; aggregate-null semantic drift. |
| Dask string dtype auto-conversion | `dask=2023.7.0`, `s=object` | `dask=2023.7.1`, `s=string` | pass | Direct only with explicit `pandas==2.0.3`, `pyarrow==12.0.1`, `numpy==1.24.4`, `partd`. |
| Polars empty Series dtype | `Float32` | `Null` | pass | Direct; schema inference edge. |
| Polars datetime component dtype | `UInt32` | `Int8` | pass | Direct; same value, dtype drift. |
| Polars outer join key preservation | columns `["k", "left", "right"]` | columns `["k", "left", "k_right", "right"]` | pass | Direct; join output-shape drift. |
| Polars NaN equality | `[true, false, true]` | `[true, true, true]` | pass | Direct; equality/dedup semantic drift. |
| pandas value_counts(sort=False) order | index `a, b, c` | index `b, a, c` | pass | Direct with Python 3.12; new side should pin `numexpr>=2.10.2` and `bottleneck>=1.4.2` for clean stderr. |
| pandas default string dtype | `object` | `str` | pass | Direct with Python 3.12; new side should pin `numexpr>=2.10.2` and `bottleneck>=1.4.2` for clean stderr. |

## Corrections From Rerun

- The behavioral claims in the original run sheet held.
- pandas 3.0 probes initially emitted optional dependency warnings in stderr
  because older `numexpr` and `bottleneck` were present. Rerunning with
  `numexpr>=2.10.2` and `bottleneck>=1.4.2` removed the warning noise and kept
  the same stdout differences.
- "Directly usable" should not mean "automatically passes the narrowest silent
  policy." It means the local package harness can reproduce the drift cleanly.
  Strict policy review still needs to mark prominent major-upgrade cases as
  `policy_sensitive`.
