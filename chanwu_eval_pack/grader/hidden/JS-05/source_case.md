# JS-05: Mongoose strictQuery stops stripping unknown filters by default

## API Or Behavior Under Test

Casting a query filter containing a field absent from the schema.

## Version Boundary

Mongoose 6.13.8 -> Mongoose 7.0.0

## Old Behavior

The unknown field is stripped from the filter.

## New Behavior

The unknown field remains in the filter.

## Why The Drift Is Silent

No database connection is needed and query casting succeeds in both versions.

## Realistic Impact Scenario

Data-access code can start issuing broader or different filters after a Mongoose major upgrade.
