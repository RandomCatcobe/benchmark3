from __future__ import annotations

import json

import io
from loguru import logger

stream = io.StringIO()
logger.remove()
logger.add(stream, serialize=True, format="{message}")
logger.info("\u96ea")
line = stream.getvalue()
print(json.dumps({"contains_escape": "\\u96ea" in line, "contains_literal": "\u96ea" in line}, sort_keys=True))
