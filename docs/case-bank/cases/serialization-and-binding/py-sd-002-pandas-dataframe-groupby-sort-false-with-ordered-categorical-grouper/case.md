# PY-SD-002: pandas DataFrame.groupby(..., sort=False) with ordered categorical grouper

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Ordered categoricals no longer force category-order sorting when `sort=False`, so aggregation index order follows input observation order.

Version boundary: `1.5.x` -> `2.0.0`.

## Why It Matters

Aggregated values are valid; only row/index order drifts.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
