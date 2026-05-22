# DOTNET-06: EF Core AsNoTracking().Include(...) query materialization

## Migration Status

The 2026-05-21 verification pass stopped at runtime, fixture, or offline-reproduction setup. It is retained as a blocked-runtime migration record.

Original run status: `blocked`.
First blocked step: `old_run/new_run`.

## Behavior Under Review

No-tracking queries stop doing identity resolution, so repeated related rows materialize as distinct object instances.

Version boundary: `EF Core 2.x` -> `3.0+`.

## Why It Matters

Query succeeds and data values match, but reference identity and graph shape differ.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
