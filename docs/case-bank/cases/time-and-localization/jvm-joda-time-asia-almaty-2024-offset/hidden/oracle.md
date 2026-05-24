# Oracle For JVM-JAVA-15

Run the probe against `joda-time:joda-time 2.12.6` and `2.12.7`.

The old run must produce `{"offset_seconds":21600}` with exit code 0 and empty stderr.

The new run must produce `{"offset_seconds":18000}` with exit code 0 and empty stderr.
