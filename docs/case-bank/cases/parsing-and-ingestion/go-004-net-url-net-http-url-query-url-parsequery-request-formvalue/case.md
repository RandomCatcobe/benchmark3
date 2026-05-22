# GO-004: net/url, net/http URL.Query, url.ParseQuery, Request.FormValue

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Query settings containing raw semicolons are no longer accepted as separators.

Version boundary: `Go <1.17` -> `Go >=1.17`.

## Why It Matters

`URL.Query()` ignores invalid semicolon-bearing settings without forcing callers to inspect an error.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
