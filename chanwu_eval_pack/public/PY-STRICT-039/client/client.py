from __future__ import annotations

import json

from wcwidth import wcwidth

print(json.dumps({
    "hangul_jungseong_filler": wcwidth("\u1160"),
    "hangul_jungseong_a": wcwidth("\u1161"),
}, sort_keys=True))
