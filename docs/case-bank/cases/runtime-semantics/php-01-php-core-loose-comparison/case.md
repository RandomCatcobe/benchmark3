# PHP-01: PHP core Loose comparison ==, !=, <=>

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Non-strict number vs non-numeric-string comparisons changed, e.g. `0 == "foo"` from `true` to `false`.

Version boundary: `PHP 7.4` -> `8.0`.

## Why It Matters

Same expression parses and runs; only branch choice/output changes.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
