# JS-10: Handlebars blocks prototype property access by default

## API Or Behavior Under Test

Template access to a property inherited from the prototype chain.

## Version Boundary

Handlebars 4.5.3 -> Handlebars 4.6.0

## Old Behavior

The inherited value renders as proto-value.

## New Behavior

The inherited value is masked and renders as an empty string.

## Why The Drift Is Silent

Template rendering succeeds and returns a string in both versions.

## Realistic Impact Scenario

Emails, reports, or generated documents can silently omit fields after a Handlebars patch upgrade.
