# PY-SD-007: Pydantic masks nested subclass fields during serialization

## API Or Behavior Under Test

Serializing a nested field annotated as a base model but holding a subclass instance.

## Version Boundary

Pydantic 1.x -> Pydantic 2.x

## Old Behavior

Both base and subclass fields are emitted.

## New Behavior

Only fields declared on the annotated base type are emitted.

## Why The Drift Is Silent

Model construction and serialization both succeed.

## Realistic Impact Scenario

API responses can silently stop exposing subclass-only fields after a Pydantic v2 migration.
