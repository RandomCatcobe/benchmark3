"""Ecosystem command implementations."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ..adapter_contracts import adapter_contract_report_json
from ..ecosystems import check_ecosystem_environment, evaluate_adapter_gates


def cmd_ecosystem_gates(args: argparse.Namespace) -> int:
    report = evaluate_adapter_gates(
        packages_root=Path(args.packages),
        audit_root=Path(args.audit),
        target_ecosystem=args.target,
        required_python_cases=args.min_python_cases,
    )
    text = report.to_json()
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if report.pass_ else 1


def cmd_ecosystem_env_check(args: argparse.Namespace) -> int:
    report = check_ecosystem_environment(args.target)
    text = report.to_json()
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if report.pass_ else 1


def cmd_ecosystem_adapters(args: argparse.Namespace) -> int:
    try:
        text = adapter_contract_report_json(args.target)
    except KeyError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0
