from __future__ import annotations

import json

from werkzeug.http import dump_cookie

print(json.dumps({"set_cookie": dump_cookie("sid", "abc")}, sort_keys=True))
