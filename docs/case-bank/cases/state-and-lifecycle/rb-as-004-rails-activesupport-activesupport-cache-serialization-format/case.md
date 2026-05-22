# RB-AS-004: Rails ActiveSupport ActiveSupport::Cache serialization format

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Default cache format version changes, altering stored bytes for the same key/value.

Version boundary: ``config.load_defaults` before 7.1` -> `7.1+`.

## Why It Matters

Reads/writes work in one runtime; persisted cache entries or byte-level tests drift.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
