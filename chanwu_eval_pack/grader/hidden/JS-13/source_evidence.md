# Evidence For JS-13

## Source URLs

- https://github.com/ajv-validator/ajv/releases/tag/v8.12.0

## Local Reproduction

- Old: `ajv 8.11.2`
- New: `ajv 8.12.0`
- Old stdout: `{"serialized":"{,\"b\":1}"}`
- New stdout: `{"serialized":"{\"b\":1}"}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/js_new_probe/js-ajv-jtd-optional-leading-comma`
