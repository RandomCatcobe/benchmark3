# Evidence For JS-11

## Source URLs

- https://github.com/npm/node-semver/releases/tag/v7.6.0

## Local Reproduction

- Old: `semver 7.5.4`
- New: `semver 7.6.0`
- Old stdout: `{"version":"1.2.3"}`
- New stdout: `{"version":"1.2.3-beta.4"}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/js_new_probe/js-semver-coerce-include-prerelease`
