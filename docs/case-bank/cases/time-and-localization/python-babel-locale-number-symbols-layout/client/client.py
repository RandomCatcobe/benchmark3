from __future__ import annotations

import json

from babel.core import Locale

symbols = Locale.parse("en").number_symbols
direct = symbols.get("decimal")
latn = symbols.get("latn")
latn_decimal = latn.get("decimal") if latn is not None else None
print(json.dumps({"direct_decimal": direct, "latn_decimal": latn_decimal, "keys": list(symbols.keys())[:6]}, sort_keys=True))
