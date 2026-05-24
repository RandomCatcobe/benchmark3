# Evidence For JVM-JAVA-11

## Source URLs

- https://github.com/jhy/jsoup/releases/tag/jsoup-1.15.4

## Source Notes

The jsoup 1.15.4 release notes describe a text extraction fix for spacing between block and inline elements.

## Local Reproduction

- Old: `org.jsoup:jsoup 1.15.3`
- New: `org.jsoup:jsoup 1.15.4`
- Old stdout: `{"text":"OneTwo"}`
- New stdout: `{"text":"One Two"}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/jvm_new_probe/jvm-jsoup-text-block-inline-spacing`
