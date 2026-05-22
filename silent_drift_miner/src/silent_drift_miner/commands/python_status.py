"""Python status command implementations."""
from __future__ import annotations

import argparse
from pathlib import Path

from ..python_status import build_python_status_report


def cmd_python_status(args: argparse.Namespace) -> int:
    report = build_python_status_report(
        cases_root=Path(args.cases),
        packages_root=Path(args.packages),
        min_audited_cases=args.min_cases,
    )
    text = report.to_json()
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if report.pass_ else 1
