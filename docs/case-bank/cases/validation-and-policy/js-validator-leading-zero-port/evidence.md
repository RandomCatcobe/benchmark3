# Evidence For JS-15

## Source URLs

- https://github.com/validatorjs/validator.js/releases/tag/13.12.0

## Local Reproduction

- Old: `validator 13.11.0`
- New: `validator 13.12.0`
- Old stdout: `{"port01":true,"port00080":true,"port80":true}`
- New stdout: `{"port01":false,"port00080":false,"port80":true}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/js_new_probe/js-validator-leading-zero-port`
