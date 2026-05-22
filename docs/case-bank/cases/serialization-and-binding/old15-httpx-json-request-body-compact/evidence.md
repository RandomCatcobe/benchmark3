# Evidence For OLD15-003

## Sources

- https://github.com/encode/httpx/blob/master/CHANGELOG.md

## Source Excerpt Or Provenance Note

0.28.0 switches JSON request serialization to a compact representation by default.

## Version Boundary

- Old version: 0.27.2
- New version: 0.28.0

## Replay Artifact

- Result: data/verification/old_15/old15-httpx-json-request-body-compact/attempt_003/result.json
- Status: verified_keep
- Diff summary: stdout changed
- First blocker: none

## Review Notes

Same local request-construction call shape; default JSON body serialization changes without a live network call.
