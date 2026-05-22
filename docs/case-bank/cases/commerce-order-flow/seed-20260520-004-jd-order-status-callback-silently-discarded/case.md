# SEED-20260520-004: JD order status callback silently discarded

## Migration Status

The 2026-05-21 verification pass could not complete the source check from this environment. It is retained as a needs-source migration record.

Original run status: `source_check_blocked`.
First blocked step: `source_check`.

## Behavior Under Review

If `orderId` does not match, the callback can return success while the order system discards the event, leaving the order stuck.

Version boundary: `verification source state` -> `unverified reproduced state`.

## Why It Matters

[JD operator interface docs](https://opendoc.jd.com/isp_all/api/interfacelist/014-commonnotifyorderstatus.html).

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
