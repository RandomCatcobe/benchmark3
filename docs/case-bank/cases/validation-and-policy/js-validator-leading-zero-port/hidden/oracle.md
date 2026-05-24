# Oracle For JS-15

Run the probe against validator 13.11.0 and validator 13.12.0.

The old run must produce `{"port01":true,"port00080":true,"port80":true}` with exit code 0 and empty stderr.

The new run must produce `{"port01":false,"port00080":false,"port80":true}` with exit code 0 and empty stderr.
