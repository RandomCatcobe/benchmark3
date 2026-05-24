# Evidence For JS-19

## Source URLs

- https://github.com/jshttp/mime-db/blob/v1.53.0/db.json

## Local Reproduction

- Old: `mime-db 1.52.0`
- New: `mime-db 1.53.0`
- Old stdout: `{"exists":false,"extensions":null}`
- New stdout: `{"exists":true,"extensions":null}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/js_new_probe/js-mime-db-parquet-media-type`
