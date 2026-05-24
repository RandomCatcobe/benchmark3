# Oracle For JS-14

Run the probe against query-string 9.2.2 and query-string 9.3.0.

The old run must produce `{"ids":["1","2"],"isArray":true}` with exit code 0 and empty stderr.

The new run must produce `{"ids":"1|2","isArray":false}` with exit code 0 and empty stderr.
