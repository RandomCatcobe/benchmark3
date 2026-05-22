# NEW-20260520-006: Mercado Libre notifications require ACK plus resource refetch

## Migration Status

The 2026-05-21 verification pass stopped at runtime, fixture, or offline-reproduction setup. It is retained as a blocked-runtime migration record.

Original run status: `blocked_offline_reproduction`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Docs describe retries if HTTP 200 is not returned promptly, advise acknowledging before fetching resource state, and provide missed-feed recovery.

Version boundary: `verification source state` -> `unverified reproduced state`.

## Why It Matters

Duplicate, delayed, or missed notifications can silently corrupt local order, inventory, or shipment state if consumers treat event delivery as final state.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
