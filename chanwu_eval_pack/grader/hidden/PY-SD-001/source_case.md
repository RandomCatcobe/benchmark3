# PY-SD-001: NumPy 2.0 changes scalar and array dtype promotion

## API Or Behavior Under Test

Promotion result for float32 values combined with Python and NumPy float64 values.

## Version Boundary

NumPy 1.26.x -> NumPy 2.0.x

## Old Behavior

The scalar expression promotes to float64 while the array expression stays float32.

## New Behavior

The scalar expression stays float32 while the array expression promotes to float64.

## Why The Drift Is Silent

Both expressions compute successfully and numeric values remain printable.

## Realistic Impact Scenario

Scientific or ML code can silently change precision, memory use, or downstream schema checks.
