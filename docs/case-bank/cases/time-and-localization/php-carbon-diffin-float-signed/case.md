# PHP-08: Carbon diffInSeconds returns signed floating-point values

## API Or Behavior Under Test

diffInSeconds for sub-second forward and reverse intervals.

## Version Boundary

Carbon 2.x -> Carbon 3.x

## Old Behavior

The method returns integer 0 for both directions.

## New Behavior

The method returns double 0.5 forward and double -0.5 reverse.

## Why The Drift Is Silent

The method call succeeds and returns a numeric value in both versions.

## Realistic Impact Scenario

Billing, scheduling, and timeout code can silently change signs and precision after a Carbon major upgrade.
