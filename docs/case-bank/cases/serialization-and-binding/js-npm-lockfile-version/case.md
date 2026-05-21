# JS-02: npm creates lockfileVersion 2 instead of version 1

## API Or Behavior Under Test

package-lock.json format generated for the same package root.

## Version Boundary

npm 6.x -> npm 7.x

## Old Behavior

npm writes lockfileVersion 1.

## New Behavior

npm writes lockfileVersion 2.

## Why The Drift Is Silent

npm install succeeds in both versions and the dependency tree is still installable.

## Realistic Impact Scenario

Tooling that parses lockfiles can silently read a different schema after a package-manager upgrade.
