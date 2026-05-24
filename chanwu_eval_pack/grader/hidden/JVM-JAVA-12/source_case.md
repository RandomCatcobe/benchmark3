# JVM-JAVA-12: Commons IO directoryContains stops matching path prefixes

## API Or Behavior Under Test

`FilenameUtils.directoryContains` from `commons-io:commons-io`.

## Version Boundary

`commons-io:commons-io` 2.11.0 -> 2.12.0.

## Old Behavior

`directoryContains("/tmp/base", "/tmp/base2/file.txt")` returns `true`.

## New Behavior

The same call returns `false`.

## Why The Drift Is Silent

The API returns a boolean in both versions with no exception or stderr output. The containment decision changes silently.

## Realistic Impact Scenario

Path allowlist or routing code can stop accepting sibling paths that only share a string prefix with an allowed directory.
