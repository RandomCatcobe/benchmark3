# Oracle For JS-17

Run the probe against is-core-module 2.8.1 and is-core-module 2.9.0.

The old run must produce `{"nodeTest18":false,"nodeTest16":false}` with exit code 0 and empty stderr.

The new run must produce `{"nodeTest18":true,"nodeTest16":false}` with exit code 0 and empty stderr.
