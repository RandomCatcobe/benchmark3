# Evidence For OLD15-007

## Sources

- https://github.com/pandas-dev/pandas/issues/55232

## Source Excerpt Or Provenance Note

read_csv no longer raises an exception for out-of-range UInt8 integers; -1 becomes 255 and 257 becomes 1.

## Version Boundary

- Old version: 1.5.3
- New version: 2.1.1

## Replay Artifact

- Result: data/verification/old_15/old15-pandas-read-csv-uint8-overflow/attempt_002/result.json
- Status: verified_keep
- Diff summary: stdout changed
- First blocker: none

## Review Notes

Same read_csv call shape; out-of-range conversion semantics changed to wrap-around values.
