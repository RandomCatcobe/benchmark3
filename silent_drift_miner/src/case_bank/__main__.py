"""Command line entrypoint for case-bank tools."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .index import build_indexes
from .pack import pack_cases
from .schema import write_metadata_schema
from .validation import validate_cases, write_expected_schema


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="case_bank")
    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser("index", help="build case-bank indexes")
    index_subparsers = index_parser.add_subparsers(dest="index_command", required=True)
    build_parser = index_subparsers.add_parser("build", help="build Markdown indexes")
    build_parser.add_argument("--cases", default="docs/case-bank/cases")
    build_parser.add_argument("--out", required=True)
    build_parser.add_argument("--schema-out", default="docs/case-bank/metadata.schema.json")
    build_parser.add_argument("--expected-schema-out", default="docs/case-bank/expected.schema.json")
    build_parser.set_defaults(func=_cmd_index_build)

    pack_parser = subparsers.add_parser("pack", help="create a public evaluation package")
    pack_parser.add_argument("--src", required=True)
    pack_parser.add_argument("--out", required=True)
    pack_parser.set_defaults(func=_cmd_pack)

    validate_parser = subparsers.add_parser("validate", help="validate case-bank source packages")
    validate_parser.add_argument("--cases", default="docs/case-bank/cases")
    validate_parser.set_defaults(func=_cmd_validate)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ValueError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1


def _cmd_index_build(args: argparse.Namespace) -> int:
    written = build_indexes(Path(args.cases), Path(args.out))
    write_metadata_schema(Path(args.schema_out))
    write_expected_schema(Path(args.expected_schema_out))
    print(f"wrote {len(written)} index files -> {args.out}")
    print(f"wrote metadata schema -> {args.schema_out}")
    print(f"wrote expected schema -> {args.expected_schema_out}")
    return 0


def _cmd_pack(args: argparse.Namespace) -> int:
    out = pack_cases(Path(args.src), Path(args.out))
    print(f"wrote evaluation package -> {out}")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    result = validate_cases(Path(args.cases))
    if result.ok:
        print(f"OK {result.checked_cases} case-bank packages validated")
        return 0
    for finding in result.findings:
        print(f"ERROR {finding}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
