# JS-20: spdx-license-ids adds pkgconf

## API Or Behavior Under Test

`spdx-license-ids` public API in the copied client probe.

## Version Boundary

spdx-license-ids 3.0.17 -> spdx-license-ids 3.0.18

## Old Behavior

The exported SPDX identifier list does not include `pkgconf`.

## New Behavior

The same list includes `pkgconf`.

## Why The Drift Is Silent

The same Node client exits 0 in both versions with empty stderr and stable JSON stdout; only the returned semantics change.

## Realistic Impact Scenario

License allow/deny checks can silently classify package metadata differently after a registry update.
