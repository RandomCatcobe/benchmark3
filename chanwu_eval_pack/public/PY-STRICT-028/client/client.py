from __future__ import annotations

import json

import re
import markdown

text = "B ref[^b] then A ref[^a]\n\n[^a]: A note\n[^b]: B note\n"
html = markdown.markdown(text, extensions=["footnotes"])
ids = re.findall(r'<li id="fn:([^"]+)"', html)
print(json.dumps({"footnote_ids": ids}, sort_keys=True))
