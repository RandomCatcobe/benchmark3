# PY-SD-003: SciPy scipy.stats.mode with omitted keepdims

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Default `keepdims` changes from legacy axis-retaining behavior to `False`, changing result shape.

Version boundary: `1.10.x` -> `1.11.0`.

## Why It Matters

`ModeResult` returns normally; broadcasting or indexing may silently target different dimensions.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
