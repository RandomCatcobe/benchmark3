from __future__ import annotations

import json

from pathlib import Path
from starlette.responses import FileResponse

path = Path(__file__)
response = FileResponse(path)
print(json.dumps({"chunk_size": response.chunk_size}, sort_keys=True))
