# Oracle For JVM-JAVA-13

Run the probe against `org.apache.commons:commons-text 1.9` and `1.10.0`.

The old run must produce `{"camel":"---"}` with exit code 0 and empty stderr.

The new run must produce `{"camel":""}` with exit code 0 and empty stderr.
