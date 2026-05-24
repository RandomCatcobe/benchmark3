# Environment For GO-011

- Runtime: Go toolchain with module download enabled.
- Package versions: `github.com/Masterminds/semver/v3 v3.3.1` and `v3.4.0`.
- Version switching: edit `client/go.mod` to require the target module version, then run `go mod tidy`.
- Adapter/API surface: library-api.
- Probe shape: run `go run .` in `client/` and parse one JSON object from stdout.
- Command shape: `cd client && go run .`.
