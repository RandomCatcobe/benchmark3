# GO-011: Masterminds semver includes prereleases across an AND range

## API Or Behavior Under Test

`(*semver.Constraints).Check` from `github.com/Masterminds/semver/v3`.

## Version Boundary

`github.com/Masterminds/semver/v3` 3.3.1 -> 3.4.0.

## Old Behavior

The constraint `>1.0.0-beta.1 <2` rejects the prerelease version `1.0.0-beta.2`.

## New Behavior

The same constraint accepts `1.0.0-beta.2`.

## Why The Drift Is Silent

The same API call returns normally in both versions. No exception, panic, stderr, or warning is emitted; only the boolean result changes.

## Realistic Impact Scenario

Release filtering code can start admitting prerelease artifacts that were previously skipped by the same semver constraint.
