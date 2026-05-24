# Evidence For JS-17

## Source URLs

- https://github.com/inspect-js/is-core-module/blob/main/CHANGELOG.md

## Local Reproduction

- Old: `is-core-module 2.8.1`
- New: `is-core-module 2.9.0`
- Old stdout: `{"nodeTest18":false,"nodeTest16":false}`
- New stdout: `{"nodeTest18":true,"nodeTest16":false}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/js_new_probe/js-is-core-module-node-test-registry`
