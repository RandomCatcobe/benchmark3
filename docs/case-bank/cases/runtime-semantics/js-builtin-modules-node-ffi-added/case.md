# JS-22: builtin-modules adds node:ffi

## API Or Behavior Under Test

`builtin-modules` public API in the copied client probe.

## Version Boundary

builtin-modules 5.1.0 -> builtin-modules 5.2.0

## Old Behavior

The exported built-in module list does not include `node:ffi`.

## New Behavior

The same list includes `node:ffi`.

## Why The Drift Is Silent

The same Node client exits 0 in both versions with empty stderr and stable JSON stdout; only the returned semantics change.

## Realistic Impact Scenario

Bundlers and dependency analyzers can silently stop treating `node:ffi` as an external package name.
