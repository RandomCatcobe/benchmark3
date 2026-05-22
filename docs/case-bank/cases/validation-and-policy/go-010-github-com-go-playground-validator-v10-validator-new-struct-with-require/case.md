# GO-010: github.com/go-playground/validator/v10 validator.New().Struct with required on struct fields

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Required validation for non-pointer struct fields is opt-in in v10 and documented as the v11 default.

Version boundary: `v10 default` -> `planned v11 default`.

## Why It Matters

Same tags and `Struct` call return a different validation result.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
