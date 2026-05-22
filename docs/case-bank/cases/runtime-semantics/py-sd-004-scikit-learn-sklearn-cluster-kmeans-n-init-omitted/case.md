# PY-SD-004: scikit-learn sklearn.cluster.KMeans(n_init omitted)

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Default `n_init` changes from `10` to `"auto"`; with `init="k-means++"` this reduces runs to 1.

Version boundary: `1.3.x` -> `1.4.0`.

## Why It Matters

Model fitting succeeds and returns plausible clusters; only model output quality/assignment drifts.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
