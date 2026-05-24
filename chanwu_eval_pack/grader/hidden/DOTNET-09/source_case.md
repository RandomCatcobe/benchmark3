# DOTNET-09: CsvHelper infers culture delimiter from CultureInfo

## API Or Behavior Under Test

CsvReader delimiter selection when the configuration is created from a semicolon culture.

## Version Boundary

CsvHelper 9.2.3 -> CsvHelper 10.0.0

## Old Behavior

The input line is read as one field, keeping A;B together.

## New Behavior

The same line is split into two fields, A and B.

## Why The Drift Is Silent

Parsing completes successfully and downstream code only sees a different row shape.

## Realistic Impact Scenario

CSV imports can silently shift columns when a deployment changes CsvHelper versions.
