# Evidence For OLD15-013

## Sources

- https://pydantic.dev/docs/validation/2.11/get-started/migration/

## Source Excerpt Or Provenance Note

A field annotated as typing.Optional[T] will be required, and will allow for a value of None. It does not mean that the field has a default value of None. (This is a breaking change from V1.)

## Version Boundary

- Old version: 1.10.15
- New version: 2.7.4

## Replay Artifact

- Result: data/verification/old_15/old15-pydantic-optional-field-required/attempt_003/result.json
- Status: verified_keep
- Diff summary: stdout changed
- First blocker: none

## Review Notes

Same public model definition; omitting a field annotated Optional[str] succeeds with an implicit None in V1 and fails as missing in V2.
