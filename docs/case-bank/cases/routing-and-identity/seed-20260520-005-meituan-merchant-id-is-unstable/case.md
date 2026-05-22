# SEED-20260520-005: Meituan merchant ID is unstable

## Migration Status

The 2026-05-21 verification pass stopped at runtime, fixture, or offline-reproduction setup. It is retained as a blocked-runtime migration record.

Original run status: `blocked_offline_reproduction`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Numeric `wm_poi_id` can change dynamically; old caches can silently point cart, menu, store, or order operations at the wrong object.

Version boundary: `verification source state` -> `unverified reproduced state`.

## Why It Matters

[Meituan enterprise waimai API](https://h5.dianping.com/app/bep-docs/sky-doc/canyinopenapi/waimai_api.html).

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
