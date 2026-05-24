# Oracle For JVM-JAVA-12

Run the probe against `commons-io:commons-io 2.11.0` and `2.12.0`.

The old run must produce `{"contains":true}` with exit code 0 and empty stderr.

The new run must produce `{"contains":false}` with exit code 0 and empty stderr.
