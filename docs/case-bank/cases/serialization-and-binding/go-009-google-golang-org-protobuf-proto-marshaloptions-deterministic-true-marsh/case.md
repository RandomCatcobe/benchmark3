# GO-009: google.golang.org/protobuf proto.MarshalOptions{Deterministic:true}.Marshal on synthetic oneofs

## Migration Status

The 2026-05-21 verification pass stopped at runtime, fixture, or offline-reproduction setup. It is retained as a blocked-runtime migration record.

Original run status: `blocked`.
First blocked step: `fixture_created`.

## Behavior Under Review

Deterministic sorting of synthetic oneofs was fixed; proto3 optional fields may produce different deterministic wire bytes/order.

Version boundary: `<v1.31.0` -> `>=v1.31.0`.

## Why It Matters

Same generated message and marshal call compile; bytes can drift without semantic message changes.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
