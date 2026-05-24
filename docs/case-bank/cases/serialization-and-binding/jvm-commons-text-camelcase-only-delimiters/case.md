# JVM-JAVA-13: Commons Text toCamelCase returns empty text for delimiter-only input

## API Or Behavior Under Test

`CaseUtils.toCamelCase` from `org.apache.commons:commons-text`.

## Version Boundary

`org.apache.commons:commons-text` 1.9 -> 1.10.0.

## Old Behavior

`CaseUtils.toCamelCase("---", false, '-', '_')` returns `"---"`.

## New Behavior

The same call returns an empty string.

## Why The Drift Is Silent

The normalization API returns normally in both versions. No warning or stderr output is emitted; only the normalized text changes.

## Realistic Impact Scenario

Key normalization code can silently change delimiter-only identifiers from a preserved sentinel-like value into an empty key.
