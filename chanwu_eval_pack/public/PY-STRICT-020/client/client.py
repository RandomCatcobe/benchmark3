from __future__ import annotations

import json

import chardet

detected = chardet.detect(b"# -*- coding: koi8-r -*-\nprint('x')\n")
print(json.dumps({"encoding": detected.get("encoding"), "confidence": detected.get("confidence")}, sort_keys=True))
