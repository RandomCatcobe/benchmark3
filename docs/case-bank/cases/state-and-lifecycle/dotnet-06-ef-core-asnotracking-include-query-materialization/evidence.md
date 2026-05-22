# Evidence For DOTNET-06

## Source Notes

- https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-3.x/breaking-changes
- docs/verification-runs/run-20260521-sequential-30.md

## Verification Ledger

- Run: `sequential_30`
- Original status: `blocked`
- First blocked step: `old_run/new_run`
- Artifact pointer: `data/verification/sequential_30/DOTNET-06`

## Outcome Note

: EF Core 2.2/3.0 dependencies restored, but both fail on .NET 10 query initialization before semantic assertion.
