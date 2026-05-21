# RB-RSP-009: RSpec aggregate_failures returns true on success

## API Or Behavior Under Test

Return value from aggregate_failures when all expectations pass.

## Version Boundary

rspec-expectations 3.10.0 -> rspec-expectations 3.11.0

## Old Behavior

The block returns nil.

## New Behavior

The block returns true.

## Why The Drift Is Silent

The expectation passes and no failure is raised in either version.

## Realistic Impact Scenario

Custom test helpers can silently change control flow if they use aggregate_failures as a truthy value.
