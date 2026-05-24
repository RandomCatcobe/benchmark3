# Oracle For GO-011

Run the probe against `github.com/Masterminds/semver/v3 v3.3.1` and `v3.4.0`.

The old run must produce `{"check":false}` with exit code 0 and empty stderr.

The new run must produce `{"check":true}` with exit code 0 and empty stderr.
