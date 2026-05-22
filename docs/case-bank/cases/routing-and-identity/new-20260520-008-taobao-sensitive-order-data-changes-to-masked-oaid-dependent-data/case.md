# NEW-20260520-008: Taobao sensitive order data changes to masked/OAID-dependent data

## Migration Status

The 2026-05-21 verification pass could not complete the source check from this environment. It is retained as a needs-source migration record.

Original run status: `source_check_blocked`.
First blocked step: `source_check`.

## Behavior Under Review

Platform docs describe receiver name, mobile, phone, and detailed address data becoming masked; OAID generation depends on specific fields.

Version boundary: `verification source state` -> `unverified reproduced state`.

## Why It Matters

Fields remain present but become masked or unusable for downstream ERP/WMS, merge-shipment, address matching, or waybill workflows unless OAID handling is implemented.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
