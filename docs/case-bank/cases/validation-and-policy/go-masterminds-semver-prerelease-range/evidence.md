# Evidence For GO-011

## Source URLs

- https://github.com/Masterminds/semver/releases/tag/v3.4.0
- https://github.com/Masterminds/semver/blob/v3.4.0/CHANGELOG.md

## Source Notes

The 3.4.0 changelog records prerelease-related constraint changes, including handling prereleases for an AND group when one constraint includes them.

## Local Reproduction

- Old: `github.com/Masterminds/semver/v3 v3.3.1`
- New: `github.com/Masterminds/semver/v3 v3.4.0`
- Old stdout: `{"check":false}`
- New stdout: `{"check":true}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/go_module_probe/go-masterminds-semver-prerelease-range`
