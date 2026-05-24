# JS-17: is-core-module recognizes node:test for Node 18

## API Or Behavior Under Test

`is-core-module` public API in the copied client probe.

## Version Boundary

is-core-module 2.8.1 -> is-core-module 2.9.0

## Old Behavior

`isCore('node:test', '18.0.0')` returns `false`.

## New Behavior

The same call returns `true`.

## Why The Drift Is Silent

The same Node client exits 0 in both versions with empty stderr and stable JSON stdout; only the returned semantics change.

## Realistic Impact Scenario

Bundler or resolver policy can silently stop treating `node:test` as an external dependency.
