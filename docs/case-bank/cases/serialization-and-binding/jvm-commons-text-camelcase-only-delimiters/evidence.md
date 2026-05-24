# Evidence For JVM-JAVA-13

## Source URLs

- https://commons.apache.org/proper/commons-text/changes.html

## Source Notes

Commons Text 1.10.0 includes a fix for `CaseUtils.toCamelCase` when the input string contains only delimiters.

## Local Reproduction

- Old: `org.apache.commons:commons-text 1.9`
- New: `org.apache.commons:commons-text 1.10.0`
- Old stdout: `{"camel":"---"}`
- New stdout: `{"camel":""}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/jvm_new_probe/jvm-commons-text-camelcase-only-delimiters`
