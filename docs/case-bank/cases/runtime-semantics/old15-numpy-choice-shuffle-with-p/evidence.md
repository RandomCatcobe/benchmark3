# Evidence For OLD15-006

## Sources

- https://github.com/numpy/numpy/issues/31210

## Source Excerpt Or Provenance Note

No source excerpt was supplied; provenance is recorded through the candidate and replay artifacts.

## Version Boundary

- Old version: 2.3.4
- New version: 2.3.5

## Replay Artifact

- Result: data/verification/old_15/old15-numpy-choice-shuffle-with-p/attempt_001/result.json
- Status: rejected_no_diff
- Diff summary: no observed difference
- First blocker: no_behavior_diff

## Review Notes

Probe ran successfully, but NumPy 2.3.4 and 2.3.5 showed no behavior diff after ignoring version metadata. Treat as current bug or parameter-semantics issue unless an old/new drift pair is identified.
