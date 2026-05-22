# JVM-JAVA-09: Maven .mvn/maven.config parsing

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked_dependency_or_runtime`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Each line in `.mvn/maven.config` is interpreted as a single argument, changing multi-option lines.

Version boundary: `3.8.x` -> `3.9.0`.

## Why It Matters

Same project config and command; effective properties can differ.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
