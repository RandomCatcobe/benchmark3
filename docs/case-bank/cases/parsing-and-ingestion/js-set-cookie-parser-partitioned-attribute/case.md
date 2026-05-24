# JS-21: set-cookie-parser recognizes Partitioned cookies

## API Or Behavior Under Test

`set-cookie-parser` public API in the copied client probe.

## Version Boundary

set-cookie-parser 2.6.0 -> set-cookie-parser 2.7.0

## Old Behavior

Parsing `Partitioned` leaves no positive `partitioned` flag.

## New Behavior

The same Set-Cookie header parses with `partitioned: true`.

## Why The Drift Is Silent

The same Node client exits 0 in both versions with empty stderr and stable JSON stdout; only the returned semantics change.

## Realistic Impact Scenario

Reverse proxies or session middleware can silently start treating the same cookie as partitioned.
