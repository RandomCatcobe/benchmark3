"""Triage command implementations."""
from __future__ import annotations

import argparse
import json
import sys

from .common import artifact_path
from .mining import load_candidates_jsonl
from ..triage import (
    build_queue_items,
    export_candidate_rows,
    find_next_item,
    load_triage_queue,
    mark_queue_item,
    queue_summary,
    write_triage_queue,
)


def cmd_triage_build(args: argparse.Namespace) -> int:
    candidates_path = artifact_path(args.candidates, args.artifact_root)
    out_path = artifact_path(args.out, args.artifact_root)
    candidates = load_candidates_jsonl(candidates_path)
    items = build_queue_items(candidates)
    write_triage_queue(items, out_path)
    print(f"wrote {len(items)} triage items -> {out_path}")
    print(json.dumps(queue_summary(items), indent=2, ensure_ascii=False))
    return 0


def cmd_triage_next(args: argparse.Namespace) -> int:
    queue_path = artifact_path(args.queue, args.artifact_root)
    items = load_triage_queue(queue_path)
    item = find_next_item(items)
    if item is None:
        print("OK no undecided candidates")
        return 0
    if args.json:
        print(json.dumps(item, ensure_ascii=False))
        return 0

    candidate = item["candidate"]
    print(f"candidate_id: {item['candidate_id']}")
    print(f"library: {candidate.get('library')}")
    print(f"version_new: {candidate.get('version_new')}")
    print(f"category: {candidate.get('category')}")
    print(f"confidence: {candidate.get('confidence')}")
    print(f"title: {candidate.get('title')}")
    evidence = candidate.get("evidence") or []
    if evidence:
        print(f"url: {evidence[0].get('url')}")
    return 0


def cmd_triage_mark(args: argparse.Namespace) -> int:
    queue_path = artifact_path(args.queue, args.artifact_root)
    try:
        items = load_triage_queue(queue_path)
        item = mark_queue_item(
            items=items,
            candidate_id=args.candidate_id,
            decision_value=args.decision,
            notes=args.notes,
            reviewer=args.reviewer,
            overwrite=args.overwrite,
        )
        write_triage_queue(items, queue_path)
    except ValueError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1

    print(f"marked {item['candidate_id']} -> {item['decision']}")
    return 0


def cmd_triage_export(args: argparse.Namespace) -> int:
    queue_path = artifact_path(args.queue, args.artifact_root)
    out_path = artifact_path(args.out, args.artifact_root)
    try:
        items = load_triage_queue(queue_path)
        rows = export_candidate_rows(
            items,
            decision_value=args.decision,
            include_undecided=args.include_undecided,
        )
    except ValueError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(row + "\n")
    print(f"exported {len(rows)} candidates -> {out_path}")
    return 0
