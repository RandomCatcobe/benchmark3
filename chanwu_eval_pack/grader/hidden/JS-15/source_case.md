# JS-15: validator rejects ports with leading zeros

## API Or Behavior Under Test

`validator` public API in the copied client probe.

## Version Boundary

validator 13.11.0 -> validator 13.12.0

## Old Behavior

`validator.isPort('01')` returns `true`.

## New Behavior

The same call returns `false`.

## Why The Drift Is Silent

The same Node client exits 0 in both versions with empty stderr and stable JSON stdout; only the returned semantics change.

## Realistic Impact Scenario

Configuration or URL validators can silently reject port strings they previously accepted.
