# Environment For GO-012

- Runtime: Go toolchain with module download enabled.
- Package versions: `github.com/pelletier/go-toml/v2 v2.2.4` and `v2.3.0`.
- Version switching: edit `client/go.mod` to require the target module version, then run `go mod tidy`.
- Adapter/API surface: library-api.
- Probe shape: run `go run .` in `client/` and parse one JSON object from stdout.
- Command shape: `cd client && go run .`.
