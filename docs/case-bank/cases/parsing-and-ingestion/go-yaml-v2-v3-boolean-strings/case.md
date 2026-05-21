# GO-007: go-yaml v3 stops treating YAML 1.1 booleans as bools

## API Or Behavior Under Test

Decoding scalar values on and no into map values.

## Version Boundary

gopkg.in/yaml.v2 -> gopkg.in/yaml.v3

## Old Behavior

YAML 1.1 boolean-like strings decode as bool true and bool false.

## New Behavior

The same scalars decode as strings.

## Why The Drift Is Silent

Unmarshal succeeds and no schema error is raised.

## Realistic Impact Scenario

Feature flags or config keys can silently change type when moving from yaml.v2 to yaml.v3.
