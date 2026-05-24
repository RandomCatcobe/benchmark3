# Evidence For PY-STRICT-022

## Sources

- https://marshmallow.readthedocs.io/en/stable/changelog.html

## Source Excerpt Or Provenance Note

marshmallow 3.12.2 restored behavior when a declared field name collides with a Schema method name.

## Version Boundary

- Old version: 3.12.1
- New version: 3.12.2

## Replay Artifact

- Result: data/verification/strict_python_new/python-marshmallow-schema-method-name-field/attempt_001/result.json
- Status: verified_keep
- Diff summary: stdout changed
- First blocker: none

## Review Notes

Generated after clean old/new local reproduction under strict silent-drift gates.
