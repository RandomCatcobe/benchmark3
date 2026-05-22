# GO-008: github.com/BurntSushi/toml toml.NewEncoder(...).Encode float output

## Migration Status

The 2026-05-21 verification pass did not promote this as an independent silent drift. It is retained as a rejected or duplicate migration record from the requested 30+50 scope.

Original run status: `no_behavior_diff`.
First blocked step: `output_assertion`.

## Behavior Under Review

Large floats are encoded using exponent syntax so values round-trip correctly; textual TOML output changes.

Version boundary: `v1.5.x` -> `v1.6.0`.

## Why It Matters

Encoding still succeeds with same API; only serialized text changes.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
