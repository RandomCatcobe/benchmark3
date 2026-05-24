# Evidence For JVM-JAVA-14

## Source URLs

- https://commons.apache.org/proper/commons-validator/changes.html

## Source Notes

Commons Validator 1.9.0 includes IBAN validator registry updates.

## Local Reproduction

- Old: `commons-validator:commons-validator 1.8.0`
- New: `commons-validator:commons-validator 1.9.0`
- Old stdout: `{"SO":false,"MN":false,"OM":false}`
- New stdout: `{"SO":true,"MN":true,"OM":true}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/jvm_new_probe/jvm-commons-validator-iban-registry-update`
