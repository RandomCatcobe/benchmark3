# PY-SD-005: Polars no longer matches null join keys by default

## API Or Behavior Under Test

Inner join behavior for rows where the join key is null.

## Version Boundary

Polars 0.19.x -> Polars 0.20.x

## Old Behavior

Null keys match, producing the null-key row plus the non-null row.

## New Behavior

Null keys do not match by default, producing only the non-null row.

## Why The Drift Is Silent

The join succeeds and returns a DataFrame in both versions.

## Realistic Impact Scenario

ETL jobs can silently lose null-key matches after a Polars upgrade.
