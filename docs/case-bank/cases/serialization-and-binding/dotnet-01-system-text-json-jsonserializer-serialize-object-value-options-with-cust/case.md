# DOTNET-01: System.Text.Json JsonSerializer.Serialize<object>(value, options) with custom JsonConverter<object>

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Root-level `object` serialization with a custom `object` converter changes from polymorphic runtime serialization to converter output.

Version boundary: `.NET 6 and earlier` -> `.NET 7`.

## Why It Matters

Same call succeeds and returns valid JSON, but payload changes.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
