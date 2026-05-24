# Oracle For GO-012

Run the probe against `github.com/pelletier/go-toml/v2 v2.2.4` and `v2.3.0`.

The old run must produce `{"toml":"count = 0\n"}` with exit code 0 and empty stderr.

The new run must produce `{"toml":""}` with exit code 0 and empty stderr.
