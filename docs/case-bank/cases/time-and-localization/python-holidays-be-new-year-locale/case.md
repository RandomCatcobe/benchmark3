# PY-HOL-002: holidays changes Belgium New Year holiday label

## API Or Behavior Under Test

Run the public client against the old and new environments.

## Version Boundary

0.28 -> 0.29

## Public Summary

Generated from old workflow artifacts.

## Replay Outcome

The old and new runs both completed and produced a meaningful behavior difference.

## Why This Is Or Is Not Silent Drift

The public call shape remains runnable on both sides.

## Why This Was Not Kept

This case is a clean silent-drift reproduction, not a failed replay. It was moved to the rejected side because `PY-HOL-015`, `PY-HOL-026`, and `PY-HOL-036` already cover the representative `holidays` drift shapes. Additional same-upstream calendar-data slices are too clustered for the keep set.
