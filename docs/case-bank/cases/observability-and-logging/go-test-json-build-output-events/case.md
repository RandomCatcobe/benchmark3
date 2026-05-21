# GO-006: go test -json emits structured build-output events

## API Or Behavior Under Test

JSON event stream produced by go test -json when the package fails to build.

## Version Boundary

Go 1.23.12 -> Go 1.26.3

## Old Behavior

Compiler diagnostics are mixed with the JSON stream as unstructured text.

## New Behavior

The build diagnostics appear as JSON events with Action=build-output and Action=build-fail.

## Why The Drift Is Silent

The command still fails, but log parsers receive a different event shape.

## Realistic Impact Scenario

CI parsers can silently drop or double-count build diagnostics after a Go toolchain upgrade.
