# RB-AS-003: Rails ActiveSupport ActiveSupport::Digest defaults

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Default digest class changes from SHA1 to SHA256.

Version boundary: ``config.load_defaults` before 7.0` -> `7.0+`.

## Why It Matters

Same digest API returns a string, but length/content changes and cache keys/checksums drift.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
