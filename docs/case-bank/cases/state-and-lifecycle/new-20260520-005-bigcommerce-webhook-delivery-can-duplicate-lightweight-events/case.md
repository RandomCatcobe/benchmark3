# NEW-20260520-005: BigCommerce webhook delivery can duplicate lightweight events

## Migration Status

The 2026-05-21 verification pass stopped at runtime, fixture, or offline-reproduction setup. It is retained as a blocked-runtime migration record.

Original run status: `blocked_offline_reproduction`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Webhook payloads are lightweight and often contain IDs; docs warn duplicate callbacks can occur from retries or network issues and apps must use idempotency.

Version boundary: `verification source state` -> `unverified reproduced state`.

## Why It Matters

A delivered webhook can cause duplicate processing or stale fetch-and-overwrite behavior unless the app dedupes and re-queries authoritative state.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
