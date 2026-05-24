from __future__ import annotations

import json

import json5

class OddInt(int):
    def __str__(self) -> str:
        return "not-json5-number"

print(json.dumps({"text": json5.dumps({"n": OddInt(7)})}, sort_keys=True))
