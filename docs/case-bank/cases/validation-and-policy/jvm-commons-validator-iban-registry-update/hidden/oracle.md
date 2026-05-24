# Oracle For JVM-JAVA-14

Run the probe against `commons-validator:commons-validator 1.8.0` and `1.9.0`.

The old run must produce `{"SO":false,"MN":false,"OM":false}` with exit code 0 and empty stderr.

The new run must produce `{"SO":true,"MN":true,"OM":true}` with exit code 0 and empty stderr.
