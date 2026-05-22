# JS-07: Tailwind CSS Utility CSS defaults for border, divide, ring

## Migration Status

The 2026-05-21 verification pass stopped at runtime, fixture, or offline-reproduction setup. It is retained as a blocked-runtime migration record.

Original run status: `blocked`.
First blocked step: `new_run`.

## Behavior Under Review

Default border/divide color changed from configured `gray-200` to `currentColor`; default ring behavior also changed.

Version boundary: `Tailwind CSS 3` -> `4`.

## Why It Matters

Same class names compile; CSS and visual output change.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
