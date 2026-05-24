# Evidence For JVM-JAVA-12

## Source URLs

- https://commons.apache.org/proper/commons-io/changes.html

## Source Notes

Commons IO 2.12.0 includes a fix for `FilenameUtils.directoryContains` path containment semantics.

## Local Reproduction

- Old: `commons-io:commons-io 2.11.0`
- New: `commons-io:commons-io 2.12.0`
- Old stdout: `{"contains":true}`
- New stdout: `{"contains":false}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/jvm_new_probe/jvm-commons-io-directory-contains-prefix`
