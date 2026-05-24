# Oracle For JS-22

Run the probe against builtin-modules 5.1.0 and builtin-modules 5.2.0.

The old run must produce `{"hasNodeFfi":false,"count":113}` with exit code 0 and empty stderr.

The new run must produce `{"hasNodeFfi":true,"count":114}` with exit code 0 and empty stderr.
