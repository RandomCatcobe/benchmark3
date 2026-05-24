# RB-STRICT-002: mime-types-data changes the Parquet content type

## API Or Behavior Under Test

`MIME::Types.type_for` with the `mime-types-data` registry.

## Version Boundary

`mime-types-data` 3.2025.0924 -> 3.2026.0317, with `mime-types` pinned.

## Old Behavior

`MIME::Types.type_for("x.parquet").first.content_type` returns `application/x-parquet`.

## New Behavior

The same call returns `application/vnd.apache.parquet`.

## Why The Drift Is Silent

The lookup succeeds in both versions with empty stderr. Only the bundled MIME registry value changes.

## Realistic Impact Scenario

Upload classification, content negotiation, or file export code can silently change a file's advertised content type after a data gem update.
