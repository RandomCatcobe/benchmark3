# JVM-JAVA-17: Tika detects warc.gz as WARC gzip media type

## API Or Behavior Under Test

`new Tika().detect("sample.warc.gz")` from `org.apache.tika:tika-core`.

## Version Boundary

`org.apache.tika:tika-core` 2.8.0 -> 2.9.0.

## Old Behavior

The filename `sample.warc.gz` is detected as `application/gzip`.

## New Behavior

The same filename is detected as `application/warc+gz`.

## Why The Drift Is Silent

The media-type detector returns normally in both versions. With an explicit no-op SLF4J provider, runtime stderr is empty and only the detected media type changes.

## Realistic Impact Scenario

Ingestion pipelines can silently route compressed WARC files to a different parser or storage policy after a minor Tika update.
