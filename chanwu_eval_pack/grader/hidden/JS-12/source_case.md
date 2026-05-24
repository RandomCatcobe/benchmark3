# JS-12: htmlparser2 treats textarea content as text

## API Or Behavior Under Test

`htmlparser2` public API in the copied client probe.

## Version Boundary

htmlparser2 9.0.0 -> htmlparser2 9.1.0

## Old Behavior

Parsing `<textarea><b>x</b></textarea>` creates a nested `b` tag child.

## New Behavior

The same input keeps `<b>x</b>` as textarea text.

## Why The Drift Is Silent

The same Node client exits 0 in both versions with empty stderr and stable JSON stdout; only the returned semantics change.

## Realistic Impact Scenario

HTML sanitizers or content extractors can silently change tree shape for textarea payloads.
