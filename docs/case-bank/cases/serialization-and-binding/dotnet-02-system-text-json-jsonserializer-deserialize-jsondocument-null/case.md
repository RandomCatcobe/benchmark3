# DOTNET-02: System.Text.Json JsonSerializer.Deserialize<JsonDocument>("null")

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

JSON `null` deserializes to `null` before, but to a non-null `JsonDocument` whose root kind is `Null` after.

Version boundary: `.NET 8 and earlier` -> `.NET 9`.

## Why It Matters

Both deserialize successfully; downstream null checks flip.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
