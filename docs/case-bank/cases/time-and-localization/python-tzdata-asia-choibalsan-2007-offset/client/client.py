from __future__ import annotations

import json

from datetime import datetime
from zoneinfo import ZoneInfo, reset_tzpath

reset_tzpath([])
dt = datetime(2007, 1, 1, 12, 0, tzinfo=ZoneInfo("Asia/Choibalsan"))
print(json.dumps({"offset_seconds": int(dt.utcoffset().total_seconds())}, sort_keys=True))
