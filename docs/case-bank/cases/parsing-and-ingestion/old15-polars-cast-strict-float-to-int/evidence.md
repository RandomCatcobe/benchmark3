# Evidence For OLD15-011

## Sources

- https://stackoverflow.com/q/78695585

## Source Excerpt Or Provenance Note

No source excerpt was supplied; provenance is recorded through the candidate and replay artifacts.

## Version Boundary

- Old version: 1.0.0
- New version: 1.30.0

## Replay Artifact

- Result: data/verification/old_15/old15-polars-cast-strict-float-to-int/attempt_001/result.json
- Status: rejected_no_diff
- Diff summary: no observed difference
- First blocker: no_behavior_diff

## Review Notes

Probe ran successfully, but Polars 1.0.0 and 1.30.0 showed no behavior diff after ignoring version metadata. Treat as stable semantics, not versioned drift, unless a better old/new pair is identified.
