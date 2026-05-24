# JVM-JAVA-14: Commons Validator adds IBAN validators for new countries

## API Or Behavior Under Test

`IBANValidator.getInstance().hasValidator(...)` from `commons-validator:commons-validator`.

## Version Boundary

`commons-validator:commons-validator` 1.8.0 -> 1.9.0.

## Old Behavior

The singleton validator reports no IBAN validators for `SO`, `MN`, or `OM`.

## New Behavior

The same calls report validators for all three country codes.

## Why The Drift Is Silent

The same public API returns booleans in both versions with no exception or warning. Only the built-in validation registry changes.

## Realistic Impact Scenario

Payment or onboarding validation can silently start accepting IBAN country codes that were previously rejected by the same application code.
