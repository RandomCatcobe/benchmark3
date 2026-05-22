# NEW-20260520-010: Google Merchant product input success is not product approval

## Migration Status

The 2026-05-21 verification pass stopped at runtime, fixture, or offline-reproduction setup. It is retained as a blocked-runtime migration record.

Original run status: `blocked_offline_reproduction`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

A successful product input write can later process into a product with normalized attributes, disapproved destinations, or item-level issues visible only through status APIs.

Version boundary: `verification source state` -> `unverified reproduced state`.

## Why It Matters

Product upload/update succeeds, but listing eligibility and final persisted product state diverge after asynchronous processing.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
