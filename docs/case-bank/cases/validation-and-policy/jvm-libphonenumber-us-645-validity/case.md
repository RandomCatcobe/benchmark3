# JVM-JAVA-16: libphonenumber starts accepting US 645 numbers

## API Or Behavior Under Test

`PhoneNumberUtil.isValidNumber` and `getNumberType` from `com.googlecode.libphonenumber:libphonenumber`.

## Version Boundary

`com.googlecode.libphonenumber:libphonenumber` 8.13.27 -> 8.13.28.

## Old Behavior

Parsing `+16455551234` returns a number that is not valid and has type `UNKNOWN`.

## New Behavior

The same parsed number is valid and has type `FIXED_LINE_OR_MOBILE`.

## Why The Drift Is Silent

The parse and validation APIs return normally in both versions. No exception or warning is emitted; only metadata-driven validity and type change.

## Realistic Impact Scenario

Signup, fraud, or contact-normalization systems can silently begin accepting a number range that was previously rejected by the same validation code.
