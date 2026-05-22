# DOTNET-07: EF Core Enums mapped inside EF JSON columns

## Migration Status

The 2026-05-21 verification pass stopped at runtime, fixture, or offline-reproduction setup. It is retained as a blocked-runtime migration record.

Original run status: `blocked`.
First blocked step: `fixture_created`.

## Behavior Under Review

Enums in JSON are stored as integers by default instead of strings.

Version boundary: `EF Core 7` -> `8`.

## Why It Matters

Save succeeds, but persisted JSON representation changes.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
