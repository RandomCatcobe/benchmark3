from __future__ import annotations

import json

import logging
from pythonjsonlogger import jsonlogger

record = logging.LogRecord("probe", logging.INFO, __file__, 1, "hello", (), None)
record.payload = b"abc"
formatter = jsonlogger.JsonFormatter("%(message)s %(payload)s")
payload = json.loads(formatter.format(record))["payload"]
print(json.dumps({"payload": payload}, sort_keys=True))
