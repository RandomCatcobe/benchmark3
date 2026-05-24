# JS-04: Jest snapshot formatting drops Object prefixes

## API Or Behavior Under Test

Default serializer output written to a Jest snapshot.

## Version Boundary

Jest 28.x -> Jest 29.x

## Old Behavior

Snapshots include Object prefixes.

## New Behavior

Snapshots omit Object prefixes and use plain object braces.

## Why The Drift Is Silent

The test passes and writes a valid snapshot in both versions.

## Realistic Impact Scenario

Snapshot-based review or approval workflows can record large diffs from a test-runner upgrade alone.
