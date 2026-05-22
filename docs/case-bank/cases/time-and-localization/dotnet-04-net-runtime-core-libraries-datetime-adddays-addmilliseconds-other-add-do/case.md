# DOTNET-04: .NET runtime core libraries DateTime.AddDays, AddMilliseconds, other Add* double overloads

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

`double` arguments are no longer rounded to the nearest millisecond; full double precision is used.

Version boundary: `.NET 6 and earlier` -> `.NET 7`.

## Why It Matters

Calls succeed and dates look valid, but ticks can differ.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
