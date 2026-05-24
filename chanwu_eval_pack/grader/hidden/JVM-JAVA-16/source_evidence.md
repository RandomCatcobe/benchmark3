# Evidence For JVM-JAVA-16

## Source URLs

- https://github.com/google/libphonenumber/releases/tag/v8.13.28

## Source Notes

The libphonenumber 8.13.28 release is a metadata update release; the local probe demonstrates the changed US 645 number validity.

## Local Reproduction

- Old: `com.googlecode.libphonenumber:libphonenumber 8.13.27`
- New: `com.googlecode.libphonenumber:libphonenumber 8.13.28`
- Old stdout: `{"valid":false,"type":"UNKNOWN"}`
- New stdout: `{"valid":true,"type":"FIXED_LINE_OR_MOBILE"}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/jvm_new_probe/jvm-libphonenumber-us-645-validity`
