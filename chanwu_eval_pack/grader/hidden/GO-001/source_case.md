# GO-001: encoding/json omitzero starts omitting zero fields

## API Or Behavior Under Test

encoding/json handling of the omitzero struct tag option.

## Version Boundary

Go 1.23.12 -> Go 1.26.3

## Old Behavior

The unknown tag option is ignored and count:0 is emitted.

## New Behavior

The tag is recognized and the zero-valued field is omitted.

## Why The Drift Is Silent

json.Marshal succeeds in both versions and returns valid JSON.

## Realistic Impact Scenario

Wire payloads can stop carrying zero values that older consumers used as explicit signals.
