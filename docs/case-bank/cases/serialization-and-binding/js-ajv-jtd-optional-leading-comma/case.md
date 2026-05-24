# JS-13: AJV JTD serializer removes leading comma for optional-only objects

## API Or Behavior Under Test

`ajv` public API in the copied client probe.

## Version Boundary

ajv 8.11.2 -> ajv 8.12.0

## Old Behavior

A JTD serializer for an object with only optional properties emits `{,"b":1}` for `{ b: 1 }`.

## New Behavior

The same serializer emits valid JSON `{"b":1}`.

## Why The Drift Is Silent

The same Node client exits 0 in both versions with empty stderr and stable JSON stdout; only the returned semantics change.

## Realistic Impact Scenario

Generated JSON payloads can silently become parseable and change downstream acceptance behavior.
