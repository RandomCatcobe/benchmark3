# Evidence For PY-STRICT-001

## Sources

- https://typer.tiangolo.com/release-notes/

## Source Excerpt Or Provenance Note

Typer 0.10.0 fixes the default value of None for CLI parameters typed as list | None when the default is None.

## Version Boundary

- Old version: 0.9.4
- New version: 0.10.0

## Replay Artifact

- Result: data/verification/python_typer_optional_list_none_default/attempt_001/result.json
- Status: verified_keep
- Diff summary: stdout changed
- First blocker: none

## Review Notes

Same local Typer app and no-argument CliRunner invocation; old Typer passes [] while new Typer preserves None. Existing verified packages were not rerun.
