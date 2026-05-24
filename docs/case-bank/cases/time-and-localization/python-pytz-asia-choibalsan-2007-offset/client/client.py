from __future__ import annotations

import json

from datetime import datetime
import pytz

zone = pytz.timezone("Asia/Choibalsan")
dt = zone.localize(datetime(2007, 1, 1, 12, 0))
print(json.dumps({"offset_seconds": int(dt.utcoffset().total_seconds()), "tzname": dt.tzname()}, sort_keys=True))
