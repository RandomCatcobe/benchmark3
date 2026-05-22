"""Autodiscovery command implementations."""
from __future__ import annotations

import argparse
from pathlib import Path

from ..autodiscovery import (
    AcceptedCard,
    IdeaCard,
    RejectedCard,
    RunLogEntry,
    append_accepted,
    append_idea,
    append_rejected,
    append_run_log,
    build_avoid_summary,
    build_readiness_report,
    build_run_brief,
    init_memory,
)


def cmd_autodiscovery_init(args: argparse.Namespace) -> int:
    init_memory(Path(args.idea_bank), Path(args.run_log))
    print(f"initialized autodiscovery markdown memory -> {args.idea_bank}, {args.run_log}")
    return 0


def cmd_autodiscovery_idea(args: argparse.Namespace) -> int:
    card = IdeaCard(
        title=args.title,
        package=args.package,
        api_surface=args.api_surface,
        versions=args.versions,
        source_url=args.source_url,
        source_section=args.source_section,
        evidence=args.evidence,
        behavior_hypothesis=args.behavior_hypothesis,
        silent_drift_reason=args.silent_drift_reason,
        reproduction_sketch=args.reproduction_sketch,
        duplicate_similar_to=args.duplicate_similar_to,
        duplicate_different_because=args.duplicate_different_because,
        risk_notes=args.risk_note,
        next_action=args.next_action,
    )
    card_id = append_idea(Path(args.idea_bank), card, card_id=args.id)
    print(f"appended idea card -> {card_id}")
    return 0


def cmd_autodiscovery_reject(args: argparse.Namespace) -> int:
    card = RejectedCard(
        title=args.title,
        package=args.package,
        api_surface=args.api_surface,
        source=args.source,
        tried_because=args.tried_because,
        rejected_because=args.rejected_because,
        future_avoid=args.future_avoid,
        future_may_try=args.future_may_try,
    )
    card_id = append_rejected(Path(args.idea_bank), card, card_id=args.id)
    print(f"appended rejected card -> {card_id}")
    return 0


def cmd_autodiscovery_accept(args: argparse.Namespace) -> int:
    card = AcceptedCard(
        case_id=args.case_id,
        package=args.package,
        api_surface=args.api_surface,
        versions=args.versions,
        source=args.source,
        reproduction_path=args.reproduction_path,
        oracle_path=args.oracle_path,
        package_path=args.package_path,
        audit_path=args.audit_path,
        why_non_duplicate=args.why_non_duplicate,
        follow_up_ideas=args.follow_up_idea,
    )
    card_id = append_accepted(Path(args.idea_bank), card, card_id=args.id)
    print(f"appended accepted card -> {card_id}")
    return 0


def cmd_autodiscovery_log(args: argparse.Namespace) -> int:
    entry = RunLogEntry(
        title=args.title,
        model_or_operator=args.model_or_operator,
        search_budget=args.search_budget,
        packages_searched=args.package_searched,
        ideas_added=args.idea_added,
        ideas_rejected=args.idea_rejected,
        promoted=args.promoted,
        accepted=args.accepted,
        notes=args.note,
    )
    append_run_log(Path(args.run_log), entry)
    print(f"appended autodiscovery run log -> {args.run_log}")
    return 0


def cmd_autodiscovery_avoid(args: argparse.Namespace) -> int:
    text = build_avoid_summary(Path(args.idea_bank))
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


def cmd_autodiscovery_readiness(args: argparse.Namespace) -> int:
    text = build_readiness_report(
        idea_bank=Path(args.idea_bank),
        run_log=Path(args.run_log),
        plan=Path(args.plan),
        run_brief=Path(args.run_brief),
    )
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


def cmd_autodiscovery_brief(args: argparse.Namespace) -> int:
    text = build_run_brief(
        idea_bank=Path(args.idea_bank),
        run_log=Path(args.run_log),
        attempts=args.attempts,
        package_focus=args.package_focus,
    )
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
        print(f"wrote autodiscovery next-run brief -> {out_path}")
    else:
        print(text)
    return 0
