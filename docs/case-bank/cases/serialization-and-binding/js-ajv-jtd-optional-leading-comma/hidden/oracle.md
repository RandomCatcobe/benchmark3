# Oracle For JS-13

Run the probe against ajv 8.11.2 and ajv 8.12.0.

The old run must produce `{"serialized":"{,\"b\":1}"}` with exit code 0 and empty stderr.

The new run must produce `{"serialized":"{\"b\":1}"}` with exit code 0 and empty stderr.
