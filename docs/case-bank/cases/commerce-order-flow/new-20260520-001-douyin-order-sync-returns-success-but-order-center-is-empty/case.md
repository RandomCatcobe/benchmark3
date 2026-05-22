# NEW-20260520-001: Douyin order sync returns success but order center is empty

## Migration Status

The 2026-05-21 verification pass stopped at runtime, fixture, or offline-reproduction setup. It is retained as a blocked-runtime migration record.

Original run status: `blocked_offline_reproduction`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Official FAQ says order sync can return success while the order center cannot show the order; causes include missing order-display whitelist, empty `item_list`, or the user not granting order-display authorization.

Version boundary: `verification source state` -> `unverified reproduced state`.

## Why It Matters

Developer-side API call is successful, but user/order-center business state is absent.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
