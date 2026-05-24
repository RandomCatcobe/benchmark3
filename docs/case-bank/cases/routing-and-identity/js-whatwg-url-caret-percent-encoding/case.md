# JS-16: whatwg-url percent-encodes caret in URL paths

## API Or Behavior Under Test

`whatwg-url` public API in the copied client probe.

## Version Boundary

whatwg-url 14.1.1 -> whatwg-url 14.2.0

## Old Behavior

Constructing a URL with path `a^b` preserves the caret in `pathname`.

## New Behavior

The same constructor percent-encodes the path caret.

## Why The Drift Is Silent

The same Node client exits 0 in both versions with empty stderr and stable JSON stdout; only the returned semantics change.

## Realistic Impact Scenario

Routing keys, cache keys, or signature bases derived from URL strings can silently change.
