# SEED-20260520-008: Ecommerce order-to-ERP sync chain evidence

## Migration Status

The 2026-05-21 verification pass could not complete the source check from this environment. It is retained as a needs-source migration record.

Original run status: `source_check_blocked`.
First blocked step: `source_check`.

## Behavior Under Review

Order pull, cleaning, SKU mapping, warehouse routing, and status writeback create natural cascade paths for silent field/status drift.

Version boundary: `verification source state` -> `unverified reproduced state`.

## Why It Matters

[AI Indeed order sync architecture](https://www.ai-indeed.com/encyclopedia/20019.html).

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
