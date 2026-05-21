# JVM-JAVA-01: Jackson XML empty elements deserialize as empty strings

## API Or Behavior Under Test

Reading an empty XML element into a JsonNode tree.

## Version Boundary

Jackson XML 2.11.x -> Jackson XML 2.12.x

## Old Behavior

The node is treated as NULL:null.

## New Behavior

The node is treated as STRING:"".

## Why The Drift Is Silent

XML parsing succeeds and produces a JsonNode in both versions.

## Realistic Impact Scenario

XML ingestion code can silently change null-handling and validation behavior.
