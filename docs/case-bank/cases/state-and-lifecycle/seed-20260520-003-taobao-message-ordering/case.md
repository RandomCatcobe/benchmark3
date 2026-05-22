# SEED-20260520-003: Taobao message ordering

## Migration Status

The 2026-05-21 verification pass could not complete the source check from this environment. It is retained as a needs-source migration record.

Original run status: `source_check_blocked`.
First blocked step: `source_check`.

## Behavior Under Review

Old state can arrive after newer state and overwrite local order, refund, stock, or customer-service state unless consumers query authoritative detail APIs.

Version boundary: `verification source state` -> `unverified reproduced state`.

## Why It Matters

[Taobao message docs](https://developer.alibaba.com/docs/doc.htm?articleId=121426&docType=1&treeId=735).

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
