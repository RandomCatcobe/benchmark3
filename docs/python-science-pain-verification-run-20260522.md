# Python Science-Pain Verification Run - 2026-05-22

This run continues Python silent-drift discovery with emphasis on scientific
computing, data analysis, numerical results, statistical tests, and visualization
or table outputs that humans are likely to care about.

## Result

- New acceptable local probes found: 10
- Strict non-yanked count: 10
- All accepted probes use local package installs, keep the same public call
  shape, exit successfully, and show changed stdout or changed returned data.
- Main pain themes:
  - Numeric linear algebra results
  - Statistical-test p-values
  - Pandas table shape, dtype, and date parsing
  - Windows dtype width in NumPy
  - Array API return types and object reductions

## Accepted Probes

| ID | Package | Versions | Pain surface | Old output | New output | Source |
| --- | --- | --- | --- | --- | --- | --- |
| PY-SCI-20260522-001 | `pandas` | `1.5.3 -> 2.0.3` | `get_dummies` one-hot dtype | dtypes `["uint8", "uint8"]`, stringified values `0/1` | dtypes `["bool", "bool"]`, stringified values `False/True` | https://pandas.pydata.org/pandas-docs/version/2.0.0/whatsnew/v2.0.0.html |
| PY-SCI-20260522-002 | `pandas` | `1.5.3 -> 2.0.3` | `DataFrameGroupBy.apply` index shape | `Int64Index` with `["0", "1", "2"]` | `MultiIndex` with `[("a", 0), ("a", 1), ("b", 2)]` | https://pandas.pydata.org/pandas-docs/version/2.0.0/whatsnew/v2.0.0.html |
| PY-SCI-20260522-003 | `pandas` | `1.5.3 -> 2.0.3` | mixed-format date parsing with `errors="coerce"` | `["2020-01-02", "2020-02-13"]` | `["2020-01-02", null]` | https://pandas.pydata.org/pandas-docs/version/2.0.0/whatsnew/v2.0.0.html |
| PY-SCI-20260522-004 | `numpy` | `1.26.4 -> 2.0.0` | `np.linalg.solve` stacked RHS interpretation | shape `[2, 2]`, values `[[1, 2], [2, 4]]` | shape `[1, 2, 2]`, values `[[[1, 4], [1, 4]]]` | https://numpy.org/devdocs/release/2.0.0-notes.html |
| PY-SCI-20260522-005 | `pandas` | `1.5.3 -> 2.0.3` | `DataFrame.quantile` default `numeric_only` | index `["x"]`, value `["2.0"]` | index `["x", "t"]`, values `["2.0", "2020-01-02 00:00:00"]` | https://pandas.pydata.org/pandas-docs/version/2.0.0/whatsnew/v2.0.0.html |
| PY-SCI-20260522-006 | `numpy` on Windows | `1.26.4 -> 2.0.0` | default integer width | `dtype="int32"`, `itemsize=4` | `dtype="int64"`, `itemsize=8` | https://numpy.org/devdocs/release/2.0.0-notes.html |
| PY-SCI-20260522-007 | `numpy` | `1.26.4 -> 2.0.0` | `np.gradient` return container | `type="list"` | `type="tuple"` | https://numpy.org/devdocs/release/2.0.0-notes.html |
| PY-SCI-20260522-008 | `numpy` | `1.26.4 -> 2.0.0` | object-array boolean reduction | `np.any(object array)` returns Python object `2` | returns boolean `np.True_` | https://numpy.org/devdocs/release/2.0.0-notes.html |
| PY-SCI-20260522-009 | `scipy` | `1.6.3 -> 1.7.3` | `stats.mannwhitneyu` default p-value method | p-value `0.04042779918502612` | p-value `0.1` | https://docs.scipy.org/doc/scipy-1.7.0/release.1.7.0.html |
| PY-SCI-20260522-010 | `numpy` | `1.26.4 -> 2.0.0` | `np.linalg.lstsq` default rank cutoff | rank `2`, solution `[1.0, 3333333333333333.5]` | rank `1`, solution `[1.0, 0.0]` | https://numpy.org/devdocs/release/2.0.0-notes.html |

## No-Diff Or Held Probes

| Package | Versions | Result | Note |
| --- | --- | --- | --- |
| `matplotlib` | `3.6.3 -> 3.7.0` | no diff | `plt.get_cmap("viridis")`, `set_bad("red")`, then re-read bad color returned transparent black in both versions for the tested fixture. |
| `scikit-learn` | `1.0.2 -> 1.1.3` | no diff | `r2_score` on constant target returned `1.0` and `0.0` in both versions once NumPy/SciPy were pinned compatibly. |
| `pandas` | `1.5.3 -> 2.0.3` | no diff | Tested `DataFrame.resample("2D").apply(lambda part: part)`; index and values matched. |
| `pandas` | `1.5.3 -> 2.0.3` | no diff | Tested `DataFrame.rank()` with numeric and string columns; columns and records matched. |
| `scipy` | `1.9.3 -> 1.10.1` | no diff | `stats.ttest_ind` repr and `has_df` probe matched for the tested fixture. |
| `scikit-learn` | `1.0.2 -> 1.1.3` | environment-only retry | Initial unpinned run hit a NumPy ABI mismatch; rerun with `numpy==1.23.5` and `scipy==1.9.3` completed and found no behavior diff. |

## Promotion Notes

- Strongest cases for human-interest review:
  - `numpy_linalg_lstsq_rank_cutoff`
  - `numpy_linalg_solve_rhs_shape`
  - `scipy_mannwhitneyu_default_method`
  - `pandas_to_datetime_consistent_format_coerce`
  - `pandas_get_dummies_bool_default`
- Policy-sensitive but real:
  - Several NumPy 2.0 items are documented under a major release, but the
    behaviors are high-value science/data pain points and reproduce cleanly.
  - The pandas 2.0 items are also explicit release-note changes; keep them in a
    science-pain bucket if the narrow silent-drift package set wants stricter
    "quietness".
