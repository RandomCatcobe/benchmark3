# Oracle For JS-21

Run the probe against set-cookie-parser 2.6.0 and set-cookie-parser 2.7.0.

The old run must produce `{"partitioned":false,"secure":true,"sameSite":"None"}` with exit code 0 and empty stderr.

The new run must produce `{"partitioned":true,"secure":true,"sameSite":"None"}` with exit code 0 and empty stderr.
