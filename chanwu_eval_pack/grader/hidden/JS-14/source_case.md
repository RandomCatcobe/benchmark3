# JS-14: query-string stops splitting encoded separator values

## API Or Behavior Under Test

`query-string` public API in the copied client probe.

## Version Boundary

query-string 9.2.2 -> query-string 9.3.0

## Old Behavior

Parsing `ids=1%7C2` with separator mode returns `ids` as `['1', '2']`.

## New Behavior

The same parse returns the scalar string `1|2`.

## Why The Drift Is Silent

The same Node client exits 0 in both versions with empty stderr and stable JSON stdout; only the returned semantics change.

## Realistic Impact Scenario

Request handlers can silently stop treating encoded separator text as multiple selected IDs.
