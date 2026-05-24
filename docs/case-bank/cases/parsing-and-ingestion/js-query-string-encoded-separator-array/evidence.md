# Evidence For JS-14

## Source URLs

- https://github.com/sindresorhus/query-string/releases/tag/v9.3.0

## Local Reproduction

- Old: `query-string 9.2.2`
- New: `query-string 9.3.0`
- Old stdout: `{"ids":["1","2"],"isArray":true}`
- New stdout: `{"ids":"1|2","isArray":false}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/js_new_probe/js-query-string-encoded-separator-array`
