# NEW-20260520-004: Adobe Commerce bulk API accepts queue entries that later fail

## Migration Status

The 2026-05-21 verification pass stopped at runtime, fixture, or offline-reproduction setup. It is retained as a blocked-runtime migration record.

Original run status: `blocked_offline_reproduction`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Bulk responses can show `errors:false` and per-request `status:"accepted"` because records were only queued; docs show accepted duplicate customer creates that later fail and require operation-status polling.

Version boundary: `verification source state` -> `unverified reproduced state`.

## Why It Matters

Transport/queue acceptance is mistaken for business success unless the integration reconciles per-operation failure status.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
