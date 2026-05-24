# GO-006: SilentDrift Evaluation Task

You are given a minimal client and environment notes for a dependency upgrade.
Determine whether the same client behavior is stable across the version boundary.

## Upgrade Boundary

- Dependency: `Go`
- Old version: `Go 1.23.12`
- New version: `Go 1.26.3`

## What To Do

Inspect `env.md` and the `client/` files, run the probe if your environment supports it, and submit a concise diagnosis.
Do not assume a drift exists; classify the case from the observable behavior.

## Diagnosis Fields

- `has_silent_drift`
- `root_dependency`
- `old_version`
- `new_version`
- `changed_behavior`
- `affected_output_fields`
- `recommended_mitigation`
