# JVM-JAVA-15: Joda-Time updates Asia/Almaty 2024 offset

## API Or Behavior Under Test

`DateTimeZone.forID("Asia/Almaty").getOffset(...)` from `joda-time:joda-time`.

## Version Boundary

`joda-time:joda-time` 2.12.6 -> 2.12.7.

## Old Behavior

At `2024-03-01T00:30:00Z`, `Asia/Almaty` reports an offset of 21600 seconds.

## New Behavior

The same zone and instant report an offset of 18000 seconds.

## Why The Drift Is Silent

The timezone API returns normally in both versions. No warning or stderr output is emitted; only the bundled timezone data result changes.

## Realistic Impact Scenario

Scheduling or settlement code using Joda-Time can silently shift local-time conversion for Kazakhstan timestamps after a patch update.
