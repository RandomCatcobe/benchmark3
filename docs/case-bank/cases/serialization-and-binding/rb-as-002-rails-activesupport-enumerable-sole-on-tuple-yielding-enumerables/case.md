# RB-AS-002: Rails ActiveSupport Enumerable#sole on tuple-yielding enumerables

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

For a one-entry hash, `sole` may change from returning only the key to returning the full key/value tuple.

Version boundary: `Rails <8.1` -> `8.1`.

## Why It Matters

The call succeeds and still returns one object, but object shape/content changes.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
