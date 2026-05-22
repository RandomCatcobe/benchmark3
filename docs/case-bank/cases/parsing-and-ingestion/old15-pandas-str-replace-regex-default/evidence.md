# Evidence For OLD15-008

## Sources

- https://pandas.pydata.org/pandas-docs/version/2.0/whatsnew/v2.0.0.html

## Source Excerpt Or Provenance Note

Change the default argument of regex for Series.str.replace() from True to False.

## Version Boundary

- Old version: 1.5.3
- New version: 2.0.3

## Replay Artifact

- Result: data/verification/old_15/old15-pandas-str-replace-regex-default/attempt_001/result.json
- Status: verified_keep
- Diff summary: stdout changed, stderr changed
- First blocker: none

## Review Notes

Same public call shape; omitting regex= changes whether a regex pattern is interpreted as a regex or a literal string.
