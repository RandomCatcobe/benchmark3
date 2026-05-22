# JVM-JAVA-10: Java stdlib default charset APIs such as new String(bytes), FileReader, Scanner

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Default charset becomes UTF-8, changing decoding/encoding on platforms that previously used legacy charsets.

Version boundary: `JDK 17` -> `JDK 18`.

## Why It Matters

Same source and public APIs; bytes decode differently at runtime.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
