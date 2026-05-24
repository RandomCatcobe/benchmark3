# Evidence For JVM-JAVA-17

## Source URLs

- https://tika.apache.org/2.9.0/

## Source Notes

The Tika 2.9.0 release includes media type detection updates, including WARC gzip detection.

## Local Reproduction

- Old: `org.apache.tika:tika-core 2.8.0`
- New: `org.apache.tika:tika-core 2.9.0`
- Old stdout: `{"warc_gz":"application/gzip"}`
- New stdout: `{"warc_gz":"application/warc+gz"}`
- Old/new exit code: 0
- Old/new stderr: empty after adding `org.slf4j:slf4j-nop`.
- Verification path: `data/verification/jvm_new_probe/jvm-tika-warc-gz-detection`
