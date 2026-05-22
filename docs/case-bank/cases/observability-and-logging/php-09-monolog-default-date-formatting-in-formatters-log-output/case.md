# PHP-09: Monolog Default date formatting in formatters/log output

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

DateTime values are formatted with timezone and microseconds unless disabled.

Version boundary: `Monolog 1.x` -> `2.0`.

## Why It Matters

Logging still succeeds; emitted log lines change, affecting parsers/snapshots.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
