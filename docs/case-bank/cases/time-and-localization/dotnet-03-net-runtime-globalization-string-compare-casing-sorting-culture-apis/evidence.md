# Evidence For DOTNET-03

## Source Notes

- https://learn.microsoft.com/en-us/dotnet/core/compatibility/globalization/5.0/icu-globalization-api
- docs/verification-runs/run-20260521-sequential-30.md

## Verification Ledger

- Run: `sequential_30`
- Original status: `blocked`
- First blocked step: `dependency_acquired`
- Artifact pointer: `docs/verification-runs/run-20260521-sequential-30.md`

## Outcome Note

Requires runnable .NET Core 3.1 vs .NET 5+ globalization pair. PATH has runtime-only 3.1/5 x86 and no matching SDK toolchain.
