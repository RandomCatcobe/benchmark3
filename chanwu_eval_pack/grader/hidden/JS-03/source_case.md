# JS-03: Prettier 3 adds trailing commas by default

## API Or Behavior Under Test

Default formatting of a multiline function call.

## Version Boundary

Prettier 2.8.8 -> Prettier 3.0.0

## Old Behavior

The final argument has no trailing comma.

## New Behavior

The final argument receives a trailing comma.

## Why The Drift Is Silent

Formatting succeeds and returns syntactically valid JavaScript in both versions.

## Realistic Impact Scenario

Snapshot, code-generation, or policy checks that compare formatted text can silently drift.
