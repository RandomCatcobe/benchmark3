# Oracle For JS-16

Run the probe against whatwg-url 14.1.1 and whatwg-url 14.2.0.

The old run must produce `{"href":"https://example.test/a^b?x=1^2","pathname":"/a^b","search":"?x=1^2"}` with exit code 0 and empty stderr.

The new run must produce `{"href":"https://example.test/a%5Eb?x=1^2","pathname":"/a%5Eb","search":"?x=1^2"}` with exit code 0 and empty stderr.
