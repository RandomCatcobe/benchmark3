# Evidence For DOTNET-07

## Source Notes

- https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-8.0/breaking-changes
- docs/verification-runs/run-20260521-sequential-30.md

## Verification Ledger

- Run: `sequential_30`
- Original status: `blocked`
- First blocked step: `fixture_created`
- Artifact pointer: `docs/verification-runs/run-20260521-sequential-30.md`

## Outcome Note

EF Core JSON enum storage needs a provider-backed relational JSON-column fixture; no deterministic provider fixture completed in this run.
