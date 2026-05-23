from __future__ import annotations

import json

from sismic.io import export_to_yaml, import_from_yaml

statechart = import_from_yaml("""
statechart:
  name: probe
  root state:
    name: root
    initial: idle
    states:
      - name: idle
""")
text = export_to_yaml(statechart)
lines = [line.strip() for line in text.splitlines() if line.strip()]
print(json.dumps({"yaml_lines": lines[:8]}, sort_keys=True))
