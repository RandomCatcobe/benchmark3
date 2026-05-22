# NEW-20260520-002: Amazon feed status hides per-record business failures

## Migration Status

The 2026-05-21 verification pass stopped at runtime, fixture, or offline-reproduction setup. It is retained as a blocked-runtime migration record.

Original run status: `blocked_offline_reproduction`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

`processingStatus=DONE` means feed processing completed; developers must retrieve the processing report to see successful records and records with errors.

Version boundary: `verification source state` -> `unverified reproduced state`.

## Why It Matters

Feed/task status looks complete while SKU, listing, inventory, refund, or adjustment records may not have taken effect.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
