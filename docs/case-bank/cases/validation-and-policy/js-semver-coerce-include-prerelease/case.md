# JS-11: semver coerce preserves prerelease when requested

## API Or Behavior Under Test

`semver` public API in the copied client probe.

## Version Boundary

semver 7.5.4 -> semver 7.6.0

## Old Behavior

`semver.coerce(..., { includePrerelease: true })` returns `1.2.3`.

## New Behavior

The same call returns `1.2.3-beta.4`.

## Why The Drift Is Silent

The same Node client exits 0 in both versions with empty stderr and stable JSON stdout; only the returned semantics change.

## Realistic Impact Scenario

Version filtering code can silently admit or preserve prerelease labels that were previously stripped.
