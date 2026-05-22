# PHP-04: Symfony Serializer CsvEncoder::decode() default context

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Default `as_collection` changed to `true`; decoding one-row CSV may return a list of rows instead of a single row array.

Version boundary: `before Symfony Serializer 7.3` -> `7.3`.

## Why It Matters

Same encoder call succeeds; array nesting/default shape changes.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
