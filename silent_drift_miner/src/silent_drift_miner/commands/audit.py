"""Audit command implementations."""
from __future__ import annotations

import argparse
import json

from .common import artifact_path
from ..audit import audit_package, write_audit_report


def cmd_audit_case(args: argparse.Namespace) -> int:
    package_dir = artifact_path(args.package, args.artifact_root)
    out_path = artifact_path(args.out, args.artifact_root)
    report = audit_package(package_dir)
    write_audit_report(report, out_path)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["pass"] else 1
