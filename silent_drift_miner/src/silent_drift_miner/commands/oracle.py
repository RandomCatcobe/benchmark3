"""Oracle command implementations."""
from __future__ import annotations

import argparse
import sys

from .common import artifact_path
from ..oracle import generate_pytest_oracle, validate_pytest_oracle


def cmd_oracle_generate(args: argparse.Namespace) -> int:
    if args.template != "pytest":
        print("ERROR only --template pytest is supported", file=sys.stderr)
        return 2
    case_path = artifact_path(args.case, args.artifact_root)
    out_dir = artifact_path(args.out, args.artifact_root)
    try:
        generate_pytest_oracle(case_path, out_dir)
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    print(f"wrote oracle -> {out_dir}")
    return 0


def cmd_oracle_validate(args: argparse.Namespace) -> int:
    oracle_path = artifact_path(args.oracle, args.artifact_root)
    try:
        result = validate_pytest_oracle(oracle_path, args.mode)
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    print(result.to_json())
    return 0 if result.pass_ else 1
