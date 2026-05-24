# JVM-JAVA-02: Gson reads enum constants using toString values

## API Or Behavior Under Test

Deserializing an enum from the value returned by its toString method.

## Version Boundary

Gson 2.8.5 -> Gson 2.8.6

## Old Behavior

The parsed enum value is null.

## New Behavior

The parsed enum value is VALUE.

## Why The Drift Is Silent

Gson deserialization completes without throwing in both versions.

## Realistic Impact Scenario

Payloads that previously became null can silently map to concrete enum values.
