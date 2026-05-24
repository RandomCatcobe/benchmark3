# Oracle For JS-18

Run the probe against cookie 0.5.0 and cookie 0.6.0.

The old run must produce `{"text":"sid=abc; Secure; SameSite=None","hasPartitioned":false}` with exit code 0 and empty stderr.

The new run must produce `{"text":"sid=abc; Secure; Partitioned; SameSite=None","hasPartitioned":true}` with exit code 0 and empty stderr.
