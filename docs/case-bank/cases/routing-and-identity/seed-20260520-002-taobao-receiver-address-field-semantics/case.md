# SEED-20260520-002: Taobao receiver address field semantics

## Migration Status

The 2026-05-21 verification pass could not complete the source check from this environment. It is retained as a needs-source migration record.

Original run status: `source_check_blocked`.
First blocked step: `source_check`.

## Behavior Under Review

`receiver_city` / `receiver_district` are not stable city/district business concepts, so ERP/WMS routing keyed only on city can pick the wrong logistics rule.

Version boundary: `verification source state` -> `unverified reproduced state`.

## Why It Matters

[Taobao Open Platform](https://developer.alibaba.com/docs/api.htm?apiId=54).

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
