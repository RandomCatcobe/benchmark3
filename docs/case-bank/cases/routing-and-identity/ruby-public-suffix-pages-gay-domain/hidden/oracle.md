# Oracle For RB-STRICT-001

Run the probe against `public_suffix 5.0.4` and `5.0.5`.

The old run must produce `{"domain":"pages.gay"}` with exit code 0 and empty stderr.

The new run must produce `{"domain":"foo.pages.gay"}` with exit code 0 and empty stderr.
