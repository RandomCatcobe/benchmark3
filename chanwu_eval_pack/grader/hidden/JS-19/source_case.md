# JS-19: mime-db adds the Apache Parquet media type

## API Or Behavior Under Test

`mime-db` public API in the copied client probe.

## Version Boundary

mime-db 1.52.0 -> mime-db 1.53.0

## Old Behavior

The MIME registry has no `application/vnd.apache.parquet` entry.

## New Behavior

The same registry lookup returns an entry for `application/vnd.apache.parquet`.

## Why The Drift Is Silent

The same Node client exits 0 in both versions with empty stderr and stable JSON stdout; only the returned semantics change.

## Realistic Impact Scenario

Upload filters, content classifiers, or serializers can silently start recognizing Parquet payloads.
