# PY-SD-008: SQLAlchemy stops autocommitting Core statements

## API Or Behavior Under Test

Executing DDL and INSERT statements on a Connection without an explicit commit.

## Version Boundary

SQLAlchemy 1.4.x -> SQLAlchemy 2.0.x

## Old Behavior

The inserted row is visible after reopening the connection.

## New Behavior

The insert is rolled back when the connection closes, leaving zero rows.

## Why The Drift Is Silent

The execute calls return successfully in both versions.

## Realistic Impact Scenario

Migration or bootstrap scripts can appear to run but persist no data after a SQLAlchemy upgrade.
