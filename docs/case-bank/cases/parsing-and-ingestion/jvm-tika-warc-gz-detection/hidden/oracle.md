# Oracle For JVM-JAVA-17

Run the probe against `org.apache.tika:tika-core 2.8.0` and `2.9.0` with `slf4j-nop` on the runtime classpath.

The old run must produce `{"warc_gz":"application/gzip"}` with exit code 0 and empty stderr.

The new run must produce `{"warc_gz":"application/warc+gz"}` with exit code 0 and empty stderr.
