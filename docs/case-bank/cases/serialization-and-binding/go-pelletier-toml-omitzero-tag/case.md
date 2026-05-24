# GO-012: go-toml omitzero tag starts omitting zero values

## API Or Behavior Under Test

`toml.Marshal` from `github.com/pelletier/go-toml/v2`.

## Version Boundary

`github.com/pelletier/go-toml/v2` 2.2.4 -> 2.3.0.

## Old Behavior

The struct tag `toml:"count,omitzero"` is not honored, so the zero-valued field is emitted as `count = 0`.

## New Behavior

The same struct and API call omit the zero-valued field, producing an empty TOML document.

## Why The Drift Is Silent

Both versions return successfully with empty stderr. The serialized payload changes without an exception or warning.

## Realistic Impact Scenario

Configuration export code can silently stop writing zero-valued fields after a patch-level module update, changing downstream defaults when files are re-read by other tools.
