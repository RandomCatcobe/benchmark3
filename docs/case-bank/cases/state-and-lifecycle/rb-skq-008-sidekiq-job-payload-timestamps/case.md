# RB-SKQ-008: Sidekiq Job payload timestamps

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

`created_at`, `enqueued_at`, `failed_at`, and `retried_at` store epoch milliseconds instead of epoch float seconds.

Version boundary: `Sidekiq 7.x` -> `8.0`.

## Why It Matters

Jobs enqueue and run; payload inspection, middleware, and metrics see different numeric units.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
