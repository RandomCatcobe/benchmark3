# Evidence For JS-21

## Source URLs

- https://github.com/nfriedly/set-cookie-parser/blob/master/README.md

## Local Reproduction

- Old: `set-cookie-parser 2.6.0`
- New: `set-cookie-parser 2.7.0`
- Old stdout: `{"partitioned":false,"secure":true,"sameSite":"None"}`
- New stdout: `{"partitioned":true,"secure":true,"sameSite":"None"}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/js_new_probe/js-set-cookie-parser-partitioned-attribute`
