from __future__ import annotations

import json

import tempfile
import runpy
from pathlib import Path
import coverage

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    module = root / "probe_module.py"
    module.write_text('"""module docs"""\nvalue = 42\n', encoding="utf-8")
    cov = coverage.Coverage(data_file=str(root / ".coverage"))
    cov.start()
    runpy.run_path(str(module))
    cov.stop()
    cov.save()
    report = root / "coverage.json"
    cov.json_report(outfile=str(report), include=[str(module)])
    data = json.loads(report.read_text(encoding="utf-8"))
    file_data = next(iter(data["files"].values()))
print(json.dumps({"executed_lines": file_data["executed_lines"], "summary": file_data["summary"]}, sort_keys=True))
