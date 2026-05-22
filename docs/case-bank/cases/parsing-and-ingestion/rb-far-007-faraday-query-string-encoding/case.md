# RB-FAR-007: Faraday Query-string encoding

## Migration Status

The 2026-05-21 verification pass did not promote this as an independent silent drift. It is retained as a rejected or duplicate migration record from the requested 30+50 scope.

Original run status: `skipped_existing_record`.
First blocked step: `none recorded`.

## Behavior Under Review

Spaces in query strings encode as `%20` instead of `+`.

Version boundary: `Faraday 1.0.0` -> `1.0.1`.

## Why It Matters

Request succeeds with the same params API; URL string and signatures differ.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
