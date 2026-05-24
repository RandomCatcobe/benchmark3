# Evidence For JVM-JAVA-15

## Source URLs

- https://www.joda.org/joda-time/changes-report.html

## Source Notes

Joda-Time 2.12.7 updates its bundled timezone data relative to 2.12.6.

## Local Reproduction

- Old: `joda-time:joda-time 2.12.6`
- New: `joda-time:joda-time 2.12.7`
- Old stdout: `{"offset_seconds":21600}`
- New stdout: `{"offset_seconds":18000}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/jvm_new_probe/jvm-joda-time-asia-almaty-2024-offset`
