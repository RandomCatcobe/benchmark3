# DOTNET-03: .NET runtime globalization string.Compare, casing, sorting, culture APIs

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Windows globalization switches from NLS to ICU, changing culture-sensitive comparisons, casing, sort keys, and normalization.

Version boundary: `.NET Core 3.1 and earlier on Windows` -> `.NET 5+ on modern Windows`.

## Why It Matters

APIs succeed; ordered output or equality decisions differ.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
