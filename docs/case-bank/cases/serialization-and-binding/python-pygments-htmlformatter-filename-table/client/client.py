from __future__ import annotations

import json

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

html = highlight('print("x")\n', PythonLexer(), HtmlFormatter(linenos="table", filename="demo.py"))
print(json.dumps({"html": html}, sort_keys=True))
