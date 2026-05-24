# Oracle For JVM-JAVA-16

Run the probe against `com.googlecode.libphonenumber:libphonenumber 8.13.27` and `8.13.28`.

The old run must produce `{"valid":false,"type":"UNKNOWN"}` with exit code 0 and empty stderr.

The new run must produce `{"valid":true,"type":"FIXED_LINE_OR_MOBILE"}` with exit code 0 and empty stderr.
