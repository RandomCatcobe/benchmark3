# Environment For GO-006

        - Old version: Go 1.23.12.
        - New version: Go 1.26.3.
        - Adapter/API surface: cli-output, test-runner.
        - Runtime: Go toolchain pair.
- Version switching: run go test -json ./... with Go 1.23.x and Go 1.24+.
- Probe shape: inspect stdout/stderr and count JSON events whose Action starts with build.
