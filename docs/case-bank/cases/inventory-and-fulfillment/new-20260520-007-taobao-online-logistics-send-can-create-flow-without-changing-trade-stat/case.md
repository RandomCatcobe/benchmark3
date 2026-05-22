# NEW-20260520-007: Taobao online logistics send can create flow without changing trade status

## Migration Status

The 2026-05-21 verification pass could not complete the source check from this environment. It is retained as a needs-source migration record.

Original run status: `source_check_blocked`.
First blocked step: `source_check`.

## Behavior Under Review

Service docs note that when no waybill number is provided, the call can start online shipment flow but the trade state will not become seller-shipped until `taobao.logistics.online.confirm` is called.

Version boundary: `verification source state` -> `unverified reproduced state`.

## Why It Matters

ERP can record "shipment API succeeded" while the platform trade is still not actually marked shipped.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
