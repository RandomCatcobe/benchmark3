from __future__ import annotations

import json

from yarl import URL

joined = URL("https://web.archive.org/web/").join(URL("./https://github.com/aio-libs/yarl"))
print(json.dumps({"joined": str(joined)}, sort_keys=True))
