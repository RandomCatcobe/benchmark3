# Evidence For JS-18

## Source URLs

- https://github.com/jshttp/cookie/releases/tag/v0.6.0

## Local Reproduction

- Old: `cookie 0.5.0`
- New: `cookie 0.6.0`
- Old stdout: `{"text":"sid=abc; Secure; SameSite=None","hasPartitioned":false}`
- New stdout: `{"text":"sid=abc; Secure; Partitioned; SameSite=None","hasPartitioned":true}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/js_new_probe/js-cookie-partitioned-serialize-option`
