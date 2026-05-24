# Evidence For JS-22

## Source URLs

- https://github.com/sindresorhus/builtin-modules/releases/tag/v5.2.0

## Local Reproduction

- Old: `builtin-modules 5.1.0`
- New: `builtin-modules 5.2.0`
- Old stdout: `{"hasNodeFfi":false,"count":113}`
- New stdout: `{"hasNodeFfi":true,"count":114}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/js_new_probe/js-builtin-modules-node-ffi-added`
