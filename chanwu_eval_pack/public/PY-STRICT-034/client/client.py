from __future__ import annotations

import json

import contextlib
import io
import structlog

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    structlog.get_logger().info("probe")
print(json.dumps({"stdout": buf.getvalue().strip()}, sort_keys=True))
