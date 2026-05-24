# Evidence For JS-12

## Source URLs

- https://github.com/fb55/htmlparser2/releases/tag/v9.1.0

## Local Reproduction

- Old: `htmlparser2 9.0.0`
- New: `htmlparser2 9.1.0`
- Old stdout: `{"childType":"tag","childName":"b","childData":null}`
- New stdout: `{"childType":"text","childName":null,"childData":"<b>x</b>"}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/js_new_probe/js-htmlparser2-textarea-special-tag`
