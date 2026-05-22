"""Benchmark packaging command implementations."""
from __future__ import annotations

import argparse
import sys

from .common import artifact_path
from ..bench import create_benchmark_package


def cmd_bench_package(args: argparse.Namespace) -> int:
    case_path = artifact_path(args.case, args.artifact_root)
    oracle_path = artifact_path(args.oracle, args.artifact_root)
    out_root = artifact_path(args.out, args.artifact_root)
    levels = [level.strip() for level in args.levels.split(",") if level.strip()]
    try:
        package_dir = create_benchmark_package(case_path, oracle_path, levels, out_root)
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    print(f"wrote benchmark package -> {package_dir}")
    return 0
