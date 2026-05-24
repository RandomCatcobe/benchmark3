# Evidence For GO-013

## Source URLs

- https://github.com/goccy/go-yaml/releases/tag/v1.18.0
- https://github.com/goccy/go-yaml/blob/v1.18.0/encode.go

## Source Notes

The v1.18.0 encoder source handles `encoding.TextMarshaler` output through string encoding.

## Local Reproduction

- Old: `github.com/goccy/go-yaml v1.17.1`
- New: `github.com/goccy/go-yaml v1.18.0`
- Old stdout: `{"yaml":"v:\n  a: b\n"}`
- New stdout: `{"yaml":"v: \"a: b\"\n"}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/go_module_probe/go-goccy-yaml-text-marshaler-string`
