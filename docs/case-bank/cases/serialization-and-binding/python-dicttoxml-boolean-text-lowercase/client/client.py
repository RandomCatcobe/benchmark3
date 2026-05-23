from __future__ import annotations

import json

from dicttoxml import dicttoxml

text = dicttoxml({"ok": True, "no": False}, attr_type=False, root=False).decode("utf-8")
print(json.dumps({"xml": text}, sort_keys=True))
