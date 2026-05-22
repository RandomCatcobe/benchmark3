# PHP-02: PHP core Sorting functions sort, usort, uasort, etc.

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Elements that compare equal may retain a different order because sorting became stable.

Version boundary: `PHP 7.4` -> `8.0`.

## Why It Matters

Calls still succeed; only ordering of equal items changes.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
