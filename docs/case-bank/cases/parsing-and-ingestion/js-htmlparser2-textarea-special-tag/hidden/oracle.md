# Oracle For JS-12

Run the probe against htmlparser2 9.0.0 and htmlparser2 9.1.0.

The old run must produce `{"childType":"tag","childName":"b","childData":null}` with exit code 0 and empty stderr.

The new run must produce `{"childType":"text","childName":null,"childData":"<b>x</b>"}` with exit code 0 and empty stderr.
