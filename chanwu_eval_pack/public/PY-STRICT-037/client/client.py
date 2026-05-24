from __future__ import annotations

import json

import arrow

value = arrow.get(2024, 1, 1, tzinfo="Europe/Paris")
tz = value.tzinfo
print(json.dumps({"tz_class": type(tz).__name__, "tz_module": type(tz).__module__}, sort_keys=True))
