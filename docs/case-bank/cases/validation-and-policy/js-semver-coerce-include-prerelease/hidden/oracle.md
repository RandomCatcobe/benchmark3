# Oracle For JS-11

Run the probe against semver 7.5.4 and semver 7.6.0.

The old run must produce `{"version":"1.2.3"}` with exit code 0 and empty stderr.

The new run must produce `{"version":"1.2.3-beta.4"}` with exit code 0 and empty stderr.
