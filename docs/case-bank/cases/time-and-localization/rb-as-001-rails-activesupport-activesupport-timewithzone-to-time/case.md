# RB-AS-001: Rails ActiveSupport ActiveSupport::TimeWithZone#to_time

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

`to_time` no longer returns system-local time; it preserves the receiver timezone.

Version boundary: `Rails <8.1` -> `8.1`.

## Why It Matters

Same method returns a `Time`; offsets or serialized strings drift.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
