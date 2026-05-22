# PHP-10: Guzzle Client request option idn_conversion default

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

International domain name conversion is disabled by default in Guzzle 7.

Version boundary: `Guzzle 6.x` -> `7.0`.

## Why It Matters

Same request setup can succeed with a mock handler; effective URI host changes.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
