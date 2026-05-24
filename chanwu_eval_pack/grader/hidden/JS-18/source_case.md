# JS-18: cookie serializes the Partitioned attribute

## API Or Behavior Under Test

`cookie` public API in the copied client probe.

## Version Boundary

cookie 0.5.0 -> cookie 0.6.0

## Old Behavior

`cookie.serialize(..., { partitioned: true })` omits the `Partitioned` attribute.

## New Behavior

The same call emits `Partitioned` in the Set-Cookie string.

## Why The Drift Is Silent

The same Node client exits 0 in both versions with empty stderr and stable JSON stdout; only the returned semantics change.

## Realistic Impact Scenario

Cookie writers can silently start sending CHIPS/partitioned-cookie attributes to clients.
