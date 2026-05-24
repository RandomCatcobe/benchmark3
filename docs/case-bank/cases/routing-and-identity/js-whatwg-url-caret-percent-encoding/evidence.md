# Evidence For JS-16

## Source URLs

- https://github.com/jsdom/whatwg-url/releases/tag/v14.2.0

## Local Reproduction

- Old: `whatwg-url 14.1.1`
- New: `whatwg-url 14.2.0`
- Old stdout: `{"href":"https://example.test/a^b?x=1^2","pathname":"/a^b","search":"?x=1^2"}`
- New stdout: `{"href":"https://example.test/a%5Eb?x=1^2","pathname":"/a%5Eb","search":"?x=1^2"}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/js_new_probe/js-whatwg-url-caret-percent-encoding`
