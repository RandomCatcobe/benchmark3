# PY-SD-009: Cython Compiler default language_level for .pyx files

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Files without explicit `language_level` now use Python 3 semantics by default, changing division and other language-level behavior.

Version boundary: `0.29.x` -> `3.0.0`.

## Why It Matters

Extension can build and import; numeric results differ at runtime.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
