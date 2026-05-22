"""Case-bank bridge command implementations."""
from __future__ import annotations

import argparse
import sys

from .common import artifact_path
from ..case_bank_writer import (
    CaseBankPackageRequest,
    create_case_bank_package,
    create_case_bank_package_from_curated,
)


def cmd_case_bank_create(args: argparse.Namespace) -> int:
    try:
        package_dir = create_case_bank_package(
            CaseBankPackageRequest(
                reproduction_result=artifact_path(args.reproduction_result, args.artifact_root),
                candidate=(
                    artifact_path(args.candidate, args.artifact_root)
                    if args.candidate
                    else None
                ),
                client=artifact_path(args.client, args.artifact_root),
                out_root=artifact_path(args.out_root, args.artifact_root),
                primary_scenario=args.primary_scenario,
                case_id=args.case_id,
                slug=args.slug,
                title=args.title,
                status=args.status,
                source_urls=list(args.source_url or []),
                source_excerpt=args.source_excerpt,
                retrieved_at=args.retrieved_at,
                ecosystem=args.ecosystem,
                languages=list(args.language or []),
                api_surfaces=list(args.api_surface or []),
                application_scenarios=list(args.application_scenario or []),
                drift_patterns=list(args.drift_pattern or []),
                failure_modes=list(args.failure_mode or []),
                determinism=args.determinism,
                external_dependencies=args.external_dependencies,
                review_notes=args.review_notes,
                overwrite=args.overwrite,
            )
        )
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    print(f"wrote case-bank package -> {package_dir}")
    return 0


def cmd_case_bank_from_curated(args: argparse.Namespace) -> int:
    try:
        package_dir = create_case_bank_package_from_curated(
            artifact_path(args.case, args.artifact_root),
            artifact_path(args.oracle, args.artifact_root),
            artifact_path(args.client, args.artifact_root),
            artifact_path(args.out_root, args.artifact_root),
            args.primary_scenario,
            slug=args.slug,
            title=args.title,
            application_scenarios=list(args.application_scenario or []),
            drift_patterns=list(args.drift_pattern or []),
            failure_modes=list(args.failure_mode or []),
            determinism=args.determinism,
            external_dependencies=args.external_dependencies,
            overwrite=args.overwrite,
        )
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    print(f"wrote case-bank package -> {package_dir}")
    return 0
