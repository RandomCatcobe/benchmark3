from __future__ import annotations

import json

from urllib3.connection import HTTPConnection

conn = HTTPConnection("example.com")
print(json.dumps({"blocksize": conn.blocksize}, sort_keys=True))
