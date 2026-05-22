# DOTNET-10: AutoMapper Mapping collections and destination member reuse, especially UseDestinationValue inheritance

## Migration Status

The 2026-05-21 verification pass did not promote this as an independent silent drift. It is retained as a rejected or duplicate migration record from the requested 30+50 scope.

Original run status: `no_behavior_diff`.
First blocked step: `output_assertion`.

## Behavior Under Review

Collections are mapped by default even without setters, and `UseDestinationValue` is inherited by default.

Version boundary: `AutoMapper 9.x` -> `10.0`.

## Why It Matters

Mapping succeeds, but destination objects or collections may be reused or mutated differently.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
