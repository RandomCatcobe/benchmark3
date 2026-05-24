# Oracle For JS-20

Run the probe against spdx-license-ids 3.0.17 and spdx-license-ids 3.0.18.

The old run must produce `{"hasPkgconf":false,"count":606}` with exit code 0 and empty stderr.

The new run must produce `{"hasPkgconf":true,"count":628}` with exit code 0 and empty stderr.
