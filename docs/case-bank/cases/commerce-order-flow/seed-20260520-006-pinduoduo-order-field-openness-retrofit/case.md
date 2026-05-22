# SEED-20260520-006: Pinduoduo order field openness retrofit

## Migration Status

The 2026-05-21 verification pass could not complete the source check from this environment. It is retained as a needs-source migration record.

Original run status: `source_check_blocked`.
First blocked step: `source_check`.

## Behavior Under Review

Fields stop returning or are replaced by system fields, shifting order, refund, SKU, and payment logic into stale/fallback paths.

Version boundary: `verification source state` -> `unverified reproduced state`.

## Why It Matters

[Kuaimai Open Platform](https://open.kuaimai.com/docs/question/%E7%B3%BB%E7%BB%9F%E5%85%AC%E5%91%8A/%E6%8B%BC%E5%A4%9A%E5%A4%9A%E8%AE%A2%E5%8D%95%E4%BF%A1%E6%81%AF%E5%BC%80%E6%94%BE%E6%94%B9%E9%80%A0%E5%85%AC%E5%91%8A/).

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
