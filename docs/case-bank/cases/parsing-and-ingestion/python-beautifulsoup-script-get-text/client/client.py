from __future__ import annotations

import json

from bs4 import BeautifulSoup

html = "<div><script>var token = 1;</script><p>Hello</p></div>"
soup = BeautifulSoup(html, "html.parser")
print(json.dumps({"script_text": soup.script.get_text(), "div_text": soup.div.get_text("|")}, sort_keys=True))
