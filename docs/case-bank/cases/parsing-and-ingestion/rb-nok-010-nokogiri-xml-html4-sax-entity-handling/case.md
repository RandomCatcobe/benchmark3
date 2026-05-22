# RB-NOK-010: Nokogiri XML/HTML4 SAX entity handling

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

External entity references no longer register SAX errors; parsed entities may surface through `reference` callback.

Version boundary: `Nokogiri <1.17` -> `1.17`.

## Why It Matters

SAX parse can complete, but handler event/error streams differ.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
