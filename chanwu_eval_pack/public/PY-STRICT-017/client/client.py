from __future__ import annotations

import json

import logging

logging.basicConfig(level=logging.INFO, force=True)
import filelock  # noqa: F401,E402

logger = logging.getLogger("filelock")
print(json.dumps({"level": logger.level, "effective_level": logger.getEffectiveLevel(), "debug_enabled": logger.isEnabledFor(logging.DEBUG)}, sort_keys=True))
