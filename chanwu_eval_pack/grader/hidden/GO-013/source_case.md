# GO-013: go-yaml encodes TextMarshaler output as a string scalar

## API Or Behavior Under Test

`yaml.Marshal` from `github.com/goccy/go-yaml` when a value implements `encoding.TextMarshaler`.

## Version Boundary

`github.com/goccy/go-yaml` 1.17.1 -> 1.18.0.

## Old Behavior

The text returned by `MarshalText` is parsed into YAML shape, so `a: b` becomes a nested mapping under `v`.

## New Behavior

The same text is emitted as a quoted scalar string: `v: "a: b"`.

## Why The Drift Is Silent

The same public API call returns successfully in both versions, with no stderr or warning output. Only the YAML representation changes.

## Realistic Impact Scenario

Configuration writers that use typed values with `MarshalText` can silently switch from structured YAML to string scalars, changing how downstream readers interpret the document.
