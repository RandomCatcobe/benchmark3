# Evidence For OLD15-012

## Sources

- https://pydantic.dev/docs/validation/2.11/get-started/migration/

## Source Excerpt Or Provenance Note

In Pydantic V1, the alias property returns the field's name when no alias is set. In Pydantic V2, this behavior has changed to return None when no alias is set.

## Version Boundary

- Old version: 1.10.15
- New version: 2.7.4

## Replay Artifact

- Result: data/verification/old_15/old15-pydantic-field-alias-none/attempt_001/result.json
- Status: verified_keep
- Diff summary: stdout changed
- First blocker: none

## Review Notes

Same public field lookup; reading alias for an unaliased model field returns the field name in V1 and null in V2.
