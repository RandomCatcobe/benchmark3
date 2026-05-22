# PHP-06: Laravel / Illuminate Collections when() / unless() conditional callback argument

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Passing a closure as the first argument now uses the closure result as the condition instead of treating the closure object as truthy.

Version boundary: `Laravel 8.x` -> `9.x`.

## Why It Matters

Same fluent call succeeds; callback branch execution changes.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
