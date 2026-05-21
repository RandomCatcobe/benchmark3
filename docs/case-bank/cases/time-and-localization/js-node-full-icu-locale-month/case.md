# JS-01: Node.js full ICU changes locale month formatting

## API Or Behavior Under Test

Intl.DateTimeFormat month formatting for Spanish.

## Version Boundary

Node.js 12.22.12 small-ICU -> Node.js 13.14.0 full-ICU

## Old Behavior

The runtime lacks the locale data and returns M01.

## New Behavior

The same API returns the Spanish month name enero.

## Why The Drift Is Silent

The formatter is constructed successfully in both runtimes.

## Realistic Impact Scenario

User-visible invoices, reports, or cache keys can change locale text without application code changes.
