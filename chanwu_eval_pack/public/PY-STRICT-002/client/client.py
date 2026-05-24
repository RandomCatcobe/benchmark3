from __future__ import annotations

import json

from jinja2 import Environment

items = [{"category": "CA"}, {"category": "ca"}, {"category": "NY"}]
template = Environment().from_string(
    '{% for group in items|groupby("category") %}{{ group.grouper }}:{{ group.list|length }};{% endfor %}'
)
print(json.dumps({"rendered": template.render(items=items)}, sort_keys=True))
