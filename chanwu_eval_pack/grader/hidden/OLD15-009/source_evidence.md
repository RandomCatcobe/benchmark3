# Evidence For OLD15-009

## Sources

- https://github.com/pandas-dev/pandas/issues/52653

## Source Excerpt Or Provenance Note

Pandas 1.5.3 returns dtype('<M8[ns]') while pandas 2.0.0 returns dtype('<M8[s]') for pd.Timestamp('2023-01-01').to_datetime64().

## Version Boundary

- Old version: 1.5.3
- New version: 2.0.3

## Replay Artifact

- Result: data/verification/old_15/old15-pandas-timestamp-to-datetime64-resolution/attempt_003/result.json
- Status: verified_keep
- Diff summary: stdout changed
- First blocker: none

## Review Notes

Same public call shape; dtype precision changes without an exception.
