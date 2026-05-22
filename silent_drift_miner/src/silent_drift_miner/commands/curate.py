"""Curated case command implementations."""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .common import artifact_path
from ..curation import create_curated_case, write_curated_case


def cmd_curate_create(args: argparse.Namespace) -> int:
    result_path = artifact_path(args.reproduction_result, args.artifact_root)
    out_path = artifact_path(args.out, args.artifact_root)
    try:
        case = create_curated_case(
            result_path,
            args.decision,
            args.case_id,
            source_url=args.source_url,
            source_excerpt=args.source_excerpt,
            retrieved_at=args.retrieved_at,
            ecosystem=args.ecosystem,
            version_old=args.version_old,
            version_new=args.version_new,
            api_surface=args.api_surface,
            review_notes=args.review_notes,
        )
        if not Path(args.reproduction_result).is_absolute():
            case.reproduction_result = os.path.relpath(result_path, start=out_path.parent)
        write_curated_case(case, out_path)
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    print(f"wrote curated case -> {out_path}")
    return 0
