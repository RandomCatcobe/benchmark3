from __future__ import annotations

import json

from sanic import Sanic

app = Sanic("probe")
print(json.dumps({"keep_alive_timeout": app.config.KEEP_ALIVE_TIMEOUT}, sort_keys=True))
