# NEW-20260520-009: Etsy webhooks carry resource pointers and may replay

## Migration Status

The 2026-05-21 verification pass stopped at runtime, fixture, or offline-reproduction setup. It is retained as a blocked-runtime migration record.

Original run status: `blocked_offline_reproduction`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Order events provide a resource URL rather than full authoritative state; retry/recovery behavior means webhook IDs and timestamps are needed for duplicate/replay handling.

Version boundary: `verification source state` -> `unverified reproduced state`.

## Why It Matters

Event delivery is not enough to update order state safely; consumers must idempotently fetch and reconcile current resource state.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
