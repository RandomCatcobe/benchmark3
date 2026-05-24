# Environment For GO-013

- Runtime: Go toolchain with module download enabled.
- Package versions: `github.com/goccy/go-yaml v1.17.1` and `v1.18.0`.
- Version switching: edit `client/go.mod` to require the target module version, then run `go mod tidy`.
- Adapter/API surface: library-api.
- Probe shape: run `go run .` in `client/` and parse one JSON object from stdout.
- Command shape: `cd client && go run .`.
