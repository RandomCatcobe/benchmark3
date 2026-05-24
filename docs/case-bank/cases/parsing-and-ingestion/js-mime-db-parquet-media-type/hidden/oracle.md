# Oracle For JS-19

Run the probe against mime-db 1.52.0 and mime-db 1.53.0.

The old run must produce `{"exists":false,"extensions":null}` with exit code 0 and empty stderr.

The new run must produce `{"exists":true,"extensions":null}` with exit code 0 and empty stderr.
