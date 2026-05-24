# Oracle For GO-013

Run the probe against `github.com/goccy/go-yaml v1.17.1` and `v1.18.0`.

The old run must produce `{"yaml":"v:\n  a: b\n"}` with exit code 0 and empty stderr.

The new run must produce `{"yaml":"v: \"a: b\"\n"}` with exit code 0 and empty stderr.
