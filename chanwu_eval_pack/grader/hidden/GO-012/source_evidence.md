# Evidence For GO-012

## Source URLs

- https://github.com/pelletier/go-toml/releases/tag/v2.3.0
- https://github.com/pelletier/go-toml/blob/v2.3.0/marshaler.go

## Source Notes

The v2.3.0 source documents and implements the `omitzero` tag option for the encoder.

## Local Reproduction

- Old: `github.com/pelletier/go-toml/v2 v2.2.4`
- New: `github.com/pelletier/go-toml/v2 v2.3.0`
- Old stdout: `{"toml":"count = 0\n"}`
- New stdout: `{"toml":""}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/go_module_probe/go-pelletier-toml-omitzero-tag`
