# Python Pipeline Drift Verification Run - 2026-05-22

This run continues Python silent-drift discovery along the data-pipeline line:
schema, dtype, null semantics, join output shape, aggregation output, and
table-order behavior that can quietly affect ETL, feature generation, and data
quality checks.

## Result

- New acceptable local probes found: 10
- Strict non-yanked count: 10
- All accepted probes install old and new package versions locally, keep the
  same public call shape, exit successfully, and produce changed stdout or
  changed returned data.
- Main pain themes:
  - schema and dtype drift
  - text column backend drift
  - aggregation null semantics
  - join output shape drift
  - value-count ordering drift

## Accepted Probes

| ID | Package | Versions | Pipeline surface | Old output | New output | Source |
| --- | --- | --- | --- | --- | --- | --- |
| PY-PIPE-20260522-001 | `pandas` | `1.5.3 -> 2.0.3` | `pd.Index(np.array(..., dtype=np.int8))` | `dtype="int64"` | `dtype="int8"` | https://pandas.pydata.org/pandas-docs/version/2.0.0/whatsnew/v2.0.0.html |
| PY-PIPE-20260522-002 | `polars` | `0.19.19 -> 0.20.0` | `Series.value_counts()` result schema | columns `["cat", "counts"]` | columns `["cat", "count"]` | https://docs.pola.rs/releases/upgrade/0.20/ |
| PY-PIPE-20260522-003 | `polars` | `0.19.19 -> 0.20.0` | `pl.col("x").count()` null semantics | group `a` count `2` | group `a` count `1` | https://docs.pola.rs/releases/upgrade/0.20/ |
| PY-PIPE-20260522-004 | `dask` | `2023.7.0 -> 2023.7.1` | `dd.from_pandas` text dtype with pandas 2 + pyarrow 12 | column `s` dtype `object` | column `s` dtype `string` | https://docs.dask.org/en/stable/changelog.html#v2023-7-1 |
| PY-PIPE-20260522-005 | `polars` | `0.19.19 -> 0.20.0` | empty `Series` default dtype | `Float32` | `Null` | https://docs.pola.rs/releases/upgrade/0.20/ |
| PY-PIPE-20260522-006 | `polars` | `0.19.19 -> 0.20.0` | `Series.dt.month()` output dtype | `UInt32` | `Int8` | https://docs.pola.rs/releases/upgrade/0.20/ |
| PY-PIPE-20260522-007 | `polars` | `0.19.19 -> 0.20.0` | outer join key preservation | columns `["k", "left", "right"]` | columns `["k", "left", "k_right", "right"]` | https://docs.pola.rs/releases/upgrade/0.20/ |
| PY-PIPE-20260522-008 | `polars` | `0.19.19 -> 0.20.0` | NaN equality in comparisons | `[true, false, true]` | `[true, true, true]` | https://docs.pola.rs/releases/upgrade/0.20/ |
| PY-PIPE-20260522-009 | `pandas` | `2.3.3 -> 3.0.0` | `DataFrame.value_counts(sort=False)` output order | `a, b, c` | first-observed order `b, a, c` | https://pandas.pydata.org/docs/whatsnew/v3.0.0.html |
| PY-PIPE-20260522-010 | `pandas` | `2.3.3 -> 3.0.0` | inferred string column dtype | `object` | `str` | https://pandas.pydata.org/docs/whatsnew/v3.0.0.html |

## Notes

- `dask==2023.7.1` was verified with `pandas==2.0.3`,
  `pyarrow==12.0.1`, `numpy==1.24.4`, and `partd`.
- pandas `3.0.0` probes were run on Python 3.12 via `uv run --python 3.12`.
- An initial Polars `Series.count()` probe was adjusted because
  `Series.count()` is not present in `0.19.19`; the accepted probe uses the
  documented `Expr.count()` path through `group_by(...).agg(pl.col("x").count())`.
- These cases are high-value pipeline candidates, but some are documented under
  prominent major-release upgrade guides. Keep a "quality" and "strict
  quietness" column separate when packaging.
