"""
End-to-end Layer-1 pipeline + CLI.

Stages:
  1. load target list from configs/targets.yaml
  2. for each target: fetch releases (and/or CHANGELOG file) via GitHub
  3. for each release section: rule-prescreen -> WEAK candidates
  4. LLM refinement (optional, gated on ANTHROPIC_API_KEY)
  5. write JSONL to data/candidates/<library>.jsonl
  6. emit summary report

Run:
    python -m silent_drift_miner.cli mine --config configs/targets.yaml
    python -m silent_drift_miner.cli mine --library spring-boot   # ad-hoc
    python -m silent_drift_miner.cli stats
"""
from __future__ import annotations

import argparse
from typing import Optional

from .autodiscovery import (
    DEFAULT_IDEA_BANK,
    DEFAULT_PLAN,
    DEFAULT_RUN_BRIEF,
    DEFAULT_RUN_LOG,
)
from .commands.audit import cmd_audit_case
from .commands.autodiscovery import (
    cmd_autodiscovery_accept,
    cmd_autodiscovery_avoid,
    cmd_autodiscovery_brief,
    cmd_autodiscovery_idea,
    cmd_autodiscovery_init,
    cmd_autodiscovery_log,
    cmd_autodiscovery_readiness,
    cmd_autodiscovery_reject,
)
from .commands.bench import cmd_bench_package
from .commands.case_bank import cmd_case_bank_create, cmd_case_bank_from_curated
from .commands.common import artifact_path
from .commands.curate import cmd_curate_create
from .commands.ecosystem import (
    cmd_ecosystem_adapters,
    cmd_ecosystem_env_check,
    cmd_ecosystem_gates,
)
from .commands.mining import (
    build_refiner,
    candidate_dir,
    candidate_file_arg,
    cmd_mine,
    cmd_show,
    cmd_stats,
    cmd_validate,
    load_candidates_jsonl,
    load_targets,
    mine_source_file,
    mine_target,
    summarize,
    write_candidates_jsonl,
)
from .commands.oracle import cmd_oracle_generate, cmd_oracle_validate
from .commands.python_status import cmd_python_status
from .commands.reproduce import (
    cmd_reproduce_generate_client,
    cmd_reproduce_plan,
    cmd_reproduce_run,
    cmd_reproduce_summarize,
)
from .commands.triage import (
    cmd_triage_build,
    cmd_triage_export,
    cmd_triage_mark,
    cmd_triage_next,
)
from .curation import CurationDecision
from .schema import TriageDecision

# ----------------------- CLI -----------------------
def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="silent-drift-miner")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_mine = sub.add_parser("mine", help="run the mining pipeline")
    p_mine.add_argument("--config", default="configs/targets.yaml")
    p_mine.add_argument("--library", default=None, help="only mine this library from config")
    p_mine.add_argument("--ecosystem", default="other", help="ecosystem for --source mining")
    p_mine.add_argument("--source", default=None, help="local changelog/release-note fixture")
    p_mine.add_argument("--source-url", default=None, help="stable provenance URL for --source")
    p_mine.add_argument("--cache-dir", default="data/raw_changelogs")
    p_mine.add_argument("--artifact-root", default=None,
                        help="artifact root; when set, outputs cannot escape this directory")
    p_mine.add_argument("--out-dir", default=None)
    p_mine.add_argument("--out", default=None, help="candidate JSONL output for single --source mining")
    p_mine.add_argument("--threshold", type=int, default=4,
                        help="rule score threshold to emit a WEAK candidate")
    llm_group = p_mine.add_mutually_exclusive_group()
    llm_group.add_argument("--use-llm", dest="llm_mode", action="store_const", const="api", default="none",
                           help="enable LLM refinement (needs ANTHROPIC_API_KEY)")
    llm_group.add_argument("--no-llm", dest="llm_mode", action="store_const", const="none",
                           help="disable LLM refinement (default)")
    llm_group.add_argument("--llm-filter", dest="llm_mode", action="store_const", const="offline",
                           help="run deterministic offline precision filter")
    p_mine.set_defaults(func=cmd_mine)

    p_stats = sub.add_parser("stats", help="print summary over all candidates")
    p_stats.add_argument("paths", nargs="*", help="candidate JSONL files or directories")
    p_stats.add_argument("--artifact-root", default=None,
                         help="artifact root; defaults candidate input to <root>/candidates")
    p_stats.add_argument("--out-dir", default=None)
    p_stats.set_defaults(func=cmd_stats)

    p_show = sub.add_parser("show", help="show candidates for one library")
    p_show.add_argument("target", help="library name or candidate JSONL file")
    p_show.add_argument("--artifact-root", default=None,
                        help="artifact root; defaults candidate input to <root>/candidates")
    p_show.add_argument("--out-dir", default=None)
    p_show.add_argument("--candidate-id", default=None)
    p_show.add_argument("--limit", type=int, default=20)
    p_show.add_argument("--only-category", default=None)
    p_show.add_argument("--min-confidence", default=None,
                        choices=["weak", "uncertain_silence", "high"])
    p_show.set_defaults(func=cmd_show)

    p_validate = sub.add_parser("validate-candidates",
                                help="validate JSONL schema and round-trip for a candidates file")
    p_validate.add_argument("path", help="path to a candidates .jsonl file")
    p_validate.set_defaults(func=cmd_validate)

    p_triage = sub.add_parser("triage", help="build and mark triage queues")
    triage_sub = p_triage.add_subparsers(dest="triage_cmd", required=True)

    p_triage_build = triage_sub.add_parser("build", help="build a triage queue from candidates")
    p_triage_build.add_argument("--artifact-root", default=None,
                                help="artifact root; outputs cannot escape this directory")
    p_triage_build.add_argument("--candidates", required=True)
    p_triage_build.add_argument("--out", required=True)
    p_triage_build.set_defaults(func=cmd_triage_build)

    p_triage_next = triage_sub.add_parser("next", help="show the next undecided candidate")
    p_triage_next.add_argument("--artifact-root", default=None,
                               help="artifact root; queue path must stay inside this directory")
    p_triage_next.add_argument("--queue", required=True)
    p_triage_next.add_argument("--json", action="store_true")
    p_triage_next.set_defaults(func=cmd_triage_next)

    decisions = [d.value for d in TriageDecision]
    p_triage_mark = triage_sub.add_parser("mark", help="mark one triage decision")
    p_triage_mark.add_argument("--artifact-root", default=None,
                               help="artifact root; queue path must stay inside this directory")
    p_triage_mark.add_argument("--queue", required=True)
    p_triage_mark.add_argument("--candidate-id", required=True)
    p_triage_mark.add_argument("--decision", required=True, choices=decisions)
    p_triage_mark.add_argument("--notes", default="")
    p_triage_mark.add_argument("--reviewer", default="")
    p_triage_mark.add_argument("--overwrite", action="store_true")
    p_triage_mark.set_defaults(func=cmd_triage_mark)

    p_triage_export = triage_sub.add_parser("export", help="export candidates from a queue")
    p_triage_export.add_argument("--artifact-root", default=None,
                                 help="artifact root; output cannot escape this directory")
    p_triage_export.add_argument("--queue", required=True)
    p_triage_export.add_argument("--out", required=True)
    p_triage_export.add_argument("--decision", choices=decisions, default=None)
    p_triage_export.add_argument("--include-undecided", action="store_true")
    p_triage_export.set_defaults(func=cmd_triage_export)

    p_reproduce = sub.add_parser("reproduce", help="plan and run reproductions")
    reproduce_sub = p_reproduce.add_subparsers(dest="reproduce_cmd", required=True)

    p_reproduce_plan = reproduce_sub.add_parser("plan", help="create a reproduction spec")
    p_reproduce_plan.add_argument("--artifact-root", default=None,
                                  help="artifact root; output cannot escape this directory")
    p_reproduce_plan.add_argument(
        "--ecosystem",
        default="python",
        choices=["python", "jvm", "js", "php", "ruby", "dotnet", "go"],
    )
    p_reproduce_plan.add_argument("--candidate-id", required=True)
    p_reproduce_plan.add_argument("--library", required=True)
    p_reproduce_plan.add_argument("--old-version", required=True)
    p_reproduce_plan.add_argument("--new-version", required=True)
    p_reproduce_plan.add_argument("--client-file", required=True)
    p_reproduce_plan.add_argument("--old-package-path", default=None,
                                  help="offline package directory added to PYTHONPATH for old run")
    p_reproduce_plan.add_argument("--new-package-path", default=None,
                                  help="offline package directory added to PYTHONPATH for new run")
    p_reproduce_plan.add_argument("--old-python-executable", default="python",
                                  help="base Python used for the old run or isolated venv")
    p_reproduce_plan.add_argument("--new-python-executable", default="python",
                                  help="base Python used for the new run or isolated venv")
    p_reproduce_plan.add_argument("--extra-package", action="append", default=[],
                                  help="additional package spec installed before both old and new library versions")
    p_reproduce_plan.add_argument("--old-extra-package", action="append", default=[],
                                  help="additional package spec installed only before the old library version")
    p_reproduce_plan.add_argument("--new-extra-package", action="append", default=[],
                                  help="additional package spec installed only before the new library version")
    p_reproduce_plan.add_argument("--ignore-json-field", action="append", default=None,
                                  help="JSON stdout field excluded from behavior comparison; repeat as needed")
    p_reproduce_plan.add_argument("--old-source-path", action="append", default=[],
                                  help="JVM old source root or source file; repeat for multiple roots")
    p_reproduce_plan.add_argument("--new-source-path", action="append", default=[],
                                  help="JVM new source root or source file; repeat for multiple roots")
    p_reproduce_plan.add_argument("--classpath", action="append", default=[],
                                  help="JVM shared classpath entry, such as a local JAR")
    p_reproduce_plan.add_argument("--old-classpath", action="append", default=[],
                                  help="JVM old-only classpath entry")
    p_reproduce_plan.add_argument("--new-classpath", action="append", default=[],
                                  help="JVM new-only classpath entry")
    p_reproduce_plan.add_argument("--resource-path", action="append", default=[],
                                  help="JVM shared resource directory placed on the runtime classpath")
    p_reproduce_plan.add_argument("--old-resource-path", action="append", default=[],
                                  help="JVM old-only resource directory")
    p_reproduce_plan.add_argument("--new-resource-path", action="append", default=[],
                                  help="JVM new-only resource directory")
    p_reproduce_plan.add_argument("--jvm-arg", action="append", default=[],
                                  help="JVM argument passed before -cp, such as -Dkey=value")
    p_reproduce_plan.add_argument("--old-jvm-arg", action="append", default=[],
                                  help="JVM old-only argument")
    p_reproduce_plan.add_argument("--new-jvm-arg", action="append", default=[],
                                  help="JVM new-only argument")
    p_reproduce_plan.add_argument("--program-arg", action="append", default=[],
                                  help="argument passed to the JVM client main class")
    p_reproduce_plan.add_argument("--old-program-arg", action="append", default=[],
                                  help="old-only argument passed to the JVM client main class")
    p_reproduce_plan.add_argument("--new-program-arg", action="append", default=[],
                                  help="new-only argument passed to the JVM client main class")
    p_reproduce_plan.add_argument("--main-class", default="DriftClient",
                                  help="JVM client main class")
    p_reproduce_plan.add_argument("--java-executable", default="java")
    p_reproduce_plan.add_argument("--javac-executable", default="javac")
    p_reproduce_plan.add_argument("--module-path", action="append", default=[],
                                  help="JS shared module path added to NODE_PATH")
    p_reproduce_plan.add_argument("--old-module-path", action="append", default=[],
                                  help="JS old-only module path added to NODE_PATH")
    p_reproduce_plan.add_argument("--new-module-path", action="append", default=[],
                                  help="JS new-only module path added to NODE_PATH")
    p_reproduce_plan.add_argument("--node-arg", action="append", default=[],
                                  help="JS shared node argument passed before the client file")
    p_reproduce_plan.add_argument("--old-node-arg", action="append", default=[],
                                  help="JS old-only node argument")
    p_reproduce_plan.add_argument("--new-node-arg", action="append", default=[],
                                  help="JS new-only node argument")
    p_reproduce_plan.add_argument("--node-executable", default="node")
    p_reproduce_plan.add_argument("--include-path", action="append", default=[],
                                  help="PHP shared include path")
    p_reproduce_plan.add_argument("--old-include-path", action="append", default=[],
                                  help="PHP old-only include path")
    p_reproduce_plan.add_argument("--new-include-path", action="append", default=[],
                                  help="PHP new-only include path")
    p_reproduce_plan.add_argument("--php-arg", action="append", default=[],
                                  help="PHP shared argument passed before -d include_path")
    p_reproduce_plan.add_argument("--old-php-arg", action="append", default=[],
                                  help="PHP old-only argument")
    p_reproduce_plan.add_argument("--new-php-arg", action="append", default=[],
                                  help="PHP new-only argument")
    p_reproduce_plan.add_argument("--php-executable", default="php")
    p_reproduce_plan.add_argument("--old-php-executable", default=None)
    p_reproduce_plan.add_argument("--new-php-executable", default=None)
    p_reproduce_plan.add_argument("--load-path", action="append", default=[],
                                  help="Ruby shared load path added to RUBYLIB/-I")
    p_reproduce_plan.add_argument("--old-load-path", action="append", default=[],
                                  help="Ruby old-only load path added to RUBYLIB/-I")
    p_reproduce_plan.add_argument("--new-load-path", action="append", default=[],
                                  help="Ruby new-only load path added to RUBYLIB/-I")
    p_reproduce_plan.add_argument("--ruby-arg", action="append", default=[],
                                  help="Ruby shared argument passed before the client file")
    p_reproduce_plan.add_argument("--old-ruby-arg", action="append", default=[],
                                  help="Ruby old-only argument")
    p_reproduce_plan.add_argument("--new-ruby-arg", action="append", default=[],
                                  help="Ruby new-only argument")
    p_reproduce_plan.add_argument("--ruby-executable", default="ruby")
    p_reproduce_plan.add_argument("--reference-path", action="append", default=[],
                                  help=".NET shared reference path exposed in DOTNET_ADAPTER_PACKAGE_PATHS")
    p_reproduce_plan.add_argument("--old-reference-path", action="append", default=[],
                                  help=".NET old-only reference path")
    p_reproduce_plan.add_argument("--new-reference-path", action="append", default=[],
                                  help=".NET new-only reference path")
    p_reproduce_plan.add_argument("--dotnet-arg", action="append", default=[],
                                  help=".NET shared argument passed before --")
    p_reproduce_plan.add_argument("--old-dotnet-arg", action="append", default=[],
                                  help=".NET old-only argument")
    p_reproduce_plan.add_argument("--new-dotnet-arg", action="append", default=[],
                                  help=".NET new-only argument")
    p_reproduce_plan.add_argument("--dotnet-executable", default="dotnet")
    p_reproduce_plan.add_argument("--dotnet-restore", action="store_true",
                                  help="allow dotnet run to perform restore instead of passing --no-restore")
    p_reproduce_plan.add_argument("--go-module-path", action="append", default=[],
                                  help="Go shared local module/reference path")
    p_reproduce_plan.add_argument("--old-go-module-path", action="append", default=[],
                                  help="Go old-only local module/reference path")
    p_reproduce_plan.add_argument("--new-go-module-path", action="append", default=[],
                                  help="Go new-only local module/reference path")
    p_reproduce_plan.add_argument("--go-arg", action="append", default=[],
                                  help="Go shared argument passed before the client package")
    p_reproduce_plan.add_argument("--old-go-arg", action="append", default=[],
                                  help="Go old-only argument")
    p_reproduce_plan.add_argument("--new-go-arg", action="append", default=[],
                                  help="Go new-only argument")
    p_reproduce_plan.add_argument("--go-executable", default="go")
    p_reproduce_plan.add_argument("--go-network", action="store_true",
                                  help="allow go run to use normal network module lookup")
    p_reproduce_plan.add_argument("--out", required=True)
    p_reproduce_plan.set_defaults(func=cmd_reproduce_plan)

    p_reproduce_run = reproduce_sub.add_parser("run", help="run old/new clients from a spec")
    p_reproduce_run.add_argument("--artifact-root", default=None,
                                 help="artifact root; output cannot escape this directory")
    p_reproduce_run.add_argument("--spec", required=True)
    p_reproduce_run.add_argument("--out", required=True)
    p_reproduce_run.add_argument("--timeout", type=int, default=30)
    p_reproduce_run.add_argument("--install", action="store_true",
                                 help="create isolated venvs and run each side's install command before the client")
    p_reproduce_run.add_argument("--venv-root", default=None,
                                 help="directory for reusable isolated reproduction venvs")
    p_reproduce_run.add_argument("--build-timeout", type=int, default=300,
                                 help="seconds allowed for venv creation and dependency install")
    p_reproduce_run.set_defaults(func=cmd_reproduce_run)

    p_reproduce_summarize = reproduce_sub.add_parser("summarize", help="summarize a reproduction result")
    p_reproduce_summarize.add_argument("--artifact-root", default=None,
                                       help="artifact root; result path must stay inside this directory")
    p_reproduce_summarize.add_argument("--result", required=True)
    p_reproduce_summarize.set_defaults(func=cmd_reproduce_summarize)

    p_reproduce_generate_client = reproduce_sub.add_parser(
        "generate-client",
        help="build leak-controlled client-generation prompt artifacts",
    )
    p_reproduce_generate_client.add_argument("--artifact-root", default=None,
                                             help="artifact root; outputs cannot escape this directory")
    p_reproduce_generate_client.add_argument("--candidate", required=True)
    p_reproduce_generate_client.add_argument("--candidate-id", required=True)
    p_reproduce_generate_client.add_argument("--redacted", action="store_true")
    p_reproduce_generate_client.add_argument("--dry-run", action="store_true",
                                             help="write a deterministic scaffold instead of calling a live LLM")
    p_reproduce_generate_client.add_argument("--provider", default="anthropic")
    p_reproduce_generate_client.add_argument("--model", default=None)
    p_reproduce_generate_client.add_argument("--allowed-import", action="append", default=[])
    p_reproduce_generate_client.add_argument("--forbidden-term", action="append", default=[])
    p_reproduce_generate_client.add_argument("--prompt-out", default=None)
    p_reproduce_generate_client.add_argument("--metadata-out", default=None)
    p_reproduce_generate_client.add_argument("--out", required=True)
    p_reproduce_generate_client.set_defaults(func=cmd_reproduce_generate_client)

    p_curate = sub.add_parser("curate", help="create curated case manifests")
    curate_sub = p_curate.add_subparsers(dest="curate_cmd", required=True)

    p_curate_create = curate_sub.add_parser("create", help="create an accepted or rejected case manifest")
    p_curate_create.add_argument("--artifact-root", default=None,
                                 help="artifact root; output cannot escape this directory")
    p_curate_create.add_argument("--reproduction-result", required=True)
    p_curate_create.add_argument("--decision", required=True,
                                 choices=[d.value for d in CurationDecision])
    p_curate_create.add_argument("--case-id", required=True)
    p_curate_create.add_argument("--source-url", default=None)
    p_curate_create.add_argument("--source-excerpt", default=None)
    p_curate_create.add_argument("--retrieved-at", default=None)
    p_curate_create.add_argument("--ecosystem", default=None)
    p_curate_create.add_argument("--version-old", default=None)
    p_curate_create.add_argument("--version-new", default=None)
    p_curate_create.add_argument("--api-surface", action="append", default=[])
    p_curate_create.add_argument("--review-notes", default=None)
    p_curate_create.add_argument("--out", required=True)
    p_curate_create.set_defaults(func=cmd_curate_create)

    p_oracle = sub.add_parser("oracle", help="generate and validate oracles")
    oracle_sub = p_oracle.add_subparsers(dest="oracle_cmd", required=True)

    p_oracle_generate = oracle_sub.add_parser("generate", help="generate a pytest oracle scaffold")
    p_oracle_generate.add_argument("--artifact-root", default=None,
                                   help="artifact root; output cannot escape this directory")
    p_oracle_generate.add_argument("--case", required=True)
    p_oracle_generate.add_argument("--template", default="pytest")
    p_oracle_generate.add_argument("--out", required=True)
    p_oracle_generate.set_defaults(func=cmd_oracle_generate)

    p_oracle_validate = oracle_sub.add_parser("validate", help="run hidden pytest oracle validation")
    p_oracle_validate.add_argument("--artifact-root", default=None,
                                   help="artifact root; oracle path must stay inside this directory")
    p_oracle_validate.add_argument("--oracle", required=True)
    p_oracle_validate.add_argument("--mode", required=True, choices=["old", "new", "fixed"])
    p_oracle_validate.set_defaults(func=cmd_oracle_validate)

    p_bench = sub.add_parser("bench", help="package benchmark tasks")
    bench_sub = p_bench.add_subparsers(dest="bench_cmd", required=True)

    p_bench_package = bench_sub.add_parser("package", help="package a curated case and oracle")
    p_bench_package.add_argument("--artifact-root", default=None,
                                 help="artifact root; output cannot escape this directory")
    p_bench_package.add_argument("--case", required=True)
    p_bench_package.add_argument("--oracle", required=True)
    p_bench_package.add_argument("--levels", default="L1,L2,L3")
    p_bench_package.add_argument("--out", required=True)
    p_bench_package.set_defaults(func=cmd_bench_package)

    p_case_bank = sub.add_parser("case-bank", help="write case-bank source packages")
    case_bank_sub = p_case_bank.add_subparsers(dest="case_bank_cmd", required=True)

    p_case_bank_create = case_bank_sub.add_parser(
        "create",
        help="create a case-bank package from candidate and reproduction artifacts",
    )
    p_case_bank_create.add_argument("--artifact-root", default=None,
                                    help="artifact root; paths cannot escape this directory")
    p_case_bank_create.add_argument("--reproduction-result", required=True)
    p_case_bank_create.add_argument("--candidate", default=None)
    p_case_bank_create.add_argument("--client", required=True)
    p_case_bank_create.add_argument("--case-id", required=True)
    p_case_bank_create.add_argument("--slug", default=None)
    p_case_bank_create.add_argument("--title", default=None)
    p_case_bank_create.add_argument("--status", default=None)
    p_case_bank_create.add_argument("--source-url", action="append", default=[])
    p_case_bank_create.add_argument("--source-excerpt", default=None)
    p_case_bank_create.add_argument("--retrieved-at", default=None)
    p_case_bank_create.add_argument("--ecosystem", default=None)
    p_case_bank_create.add_argument("--language", action="append", default=[])
    p_case_bank_create.add_argument("--api-surface", action="append", default=[])
    p_case_bank_create.add_argument("--primary-scenario", required=True)
    p_case_bank_create.add_argument("--application-scenario", action="append", default=[])
    p_case_bank_create.add_argument("--drift-pattern", action="append", default=[])
    p_case_bank_create.add_argument("--failure-mode", action="append", default=[])
    p_case_bank_create.add_argument("--determinism", default="local-deterministic")
    p_case_bank_create.add_argument("--external-dependencies", default="package-cache")
    p_case_bank_create.add_argument("--review-notes", default=None)
    p_case_bank_create.add_argument("--out-root", required=True)
    p_case_bank_create.add_argument("--overwrite", action="store_true")
    p_case_bank_create.set_defaults(func=cmd_case_bank_create)

    p_case_bank_curated = case_bank_sub.add_parser(
        "from-curated",
        help="create a case-bank package from a curated case and oracle spec",
    )
    p_case_bank_curated.add_argument("--artifact-root", default=None,
                                     help="artifact root; paths cannot escape this directory")
    p_case_bank_curated.add_argument("--case", required=True)
    p_case_bank_curated.add_argument("--oracle", required=True)
    p_case_bank_curated.add_argument("--client", required=True)
    p_case_bank_curated.add_argument("--primary-scenario", required=True)
    p_case_bank_curated.add_argument("--application-scenario", action="append", default=[])
    p_case_bank_curated.add_argument("--drift-pattern", action="append", default=[])
    p_case_bank_curated.add_argument("--failure-mode", action="append", default=[])
    p_case_bank_curated.add_argument("--determinism", default="local-deterministic")
    p_case_bank_curated.add_argument("--external-dependencies", default="package-cache")
    p_case_bank_curated.add_argument("--slug", default=None)
    p_case_bank_curated.add_argument("--title", default=None)
    p_case_bank_curated.add_argument("--out-root", required=True)
    p_case_bank_curated.add_argument("--overwrite", action="store_true")
    p_case_bank_curated.set_defaults(func=cmd_case_bank_from_curated)

    p_audit = sub.add_parser("audit", help="audit packaged benchmark tasks")
    audit_sub = p_audit.add_subparsers(dest="audit_cmd", required=True)

    p_audit_case = audit_sub.add_parser("case", help="audit one benchmark package")
    p_audit_case.add_argument("--artifact-root", default=None,
                              help="artifact root; output cannot escape this directory")
    p_audit_case.add_argument("--package", required=True)
    p_audit_case.add_argument("--out", required=True)
    p_audit_case.set_defaults(func=cmd_audit_case)

    p_ecosystem = sub.add_parser("ecosystem", help="inspect ecosystem expansion gates")
    ecosystem_sub = p_ecosystem.add_subparsers(dest="ecosystem_cmd", required=True)

    p_ecosystem_gates = ecosystem_sub.add_parser("gates", help="check whether a new adapter can be enabled")
    p_ecosystem_gates.add_argument("--target", required=True, help="target ecosystem, e.g. jvm")
    p_ecosystem_gates.add_argument("--packages", default="data/packages")
    p_ecosystem_gates.add_argument("--audit", default="data/audit")
    p_ecosystem_gates.add_argument("--min-python-cases", type=int, default=3)
    p_ecosystem_gates.add_argument("--out", default=None)
    p_ecosystem_gates.set_defaults(func=cmd_ecosystem_gates)

    p_ecosystem_env = ecosystem_sub.add_parser("env-check", help="check local tools for an ecosystem adapter")
    p_ecosystem_env.add_argument("--target", required=True, help="target ecosystem, e.g. jvm")
    p_ecosystem_env.add_argument("--out", default=None)
    p_ecosystem_env.set_defaults(func=cmd_ecosystem_env_check)

    p_ecosystem_adapters = ecosystem_sub.add_parser(
        "adapters",
        help="list ecosystem adapter contracts",
    )
    p_ecosystem_adapters.add_argument("--target", default=None, help="optional ecosystem filter")
    p_ecosystem_adapters.add_argument("--out", default=None)
    p_ecosystem_adapters.set_defaults(func=cmd_ecosystem_adapters)

    p_python = sub.add_parser("python", help="inspect Python-only benchmark lifecycle status")
    python_sub = p_python.add_subparsers(dest="python_cmd", required=True)

    p_python_status = python_sub.add_parser("status", help="report Python lifecycle completion")
    p_python_status.add_argument("--cases", default="cases")
    p_python_status.add_argument("--packages", default="data/packages")
    p_python_status.add_argument("--min-cases", type=int, default=3)
    p_python_status.add_argument("--out", default=None)
    p_python_status.set_defaults(func=cmd_python_status)

    p_autodiscovery = sub.add_parser(
        "autodiscovery",
        help="maintain Markdown memory for Python drift discovery",
    )
    autodiscovery_sub = p_autodiscovery.add_subparsers(dest="autodiscovery_cmd", required=True)

    p_autodiscovery_init = autodiscovery_sub.add_parser(
        "init",
        help="create the Markdown idea bank and run log if missing",
    )
    p_autodiscovery_init.add_argument("--idea-bank", default=str(DEFAULT_IDEA_BANK))
    p_autodiscovery_init.add_argument("--run-log", default=str(DEFAULT_RUN_LOG))
    p_autodiscovery_init.set_defaults(func=cmd_autodiscovery_init)

    p_autodiscovery_idea = autodiscovery_sub.add_parser("idea", help="append a discovered idea card")
    p_autodiscovery_idea.add_argument("--idea-bank", default=str(DEFAULT_IDEA_BANK))
    p_autodiscovery_idea.add_argument("--id", default=None, help="optional stable card id")
    p_autodiscovery_idea.add_argument("--title", required=True)
    p_autodiscovery_idea.add_argument("--package", default="")
    p_autodiscovery_idea.add_argument("--api-surface", default="")
    p_autodiscovery_idea.add_argument("--versions", default="")
    p_autodiscovery_idea.add_argument("--source-url", default="")
    p_autodiscovery_idea.add_argument("--source-section", default="")
    p_autodiscovery_idea.add_argument("--evidence", default="")
    p_autodiscovery_idea.add_argument("--behavior-hypothesis", default="")
    p_autodiscovery_idea.add_argument("--silent-drift-reason", default="")
    p_autodiscovery_idea.add_argument("--reproduction-sketch", default="")
    p_autodiscovery_idea.add_argument("--duplicate-similar-to", default="")
    p_autodiscovery_idea.add_argument("--duplicate-different-because", default="")
    p_autodiscovery_idea.add_argument("--risk-note", action="append", default=[])
    p_autodiscovery_idea.add_argument("--next-action", default="")
    p_autodiscovery_idea.set_defaults(func=cmd_autodiscovery_idea)

    p_autodiscovery_reject = autodiscovery_sub.add_parser("reject", help="append a rejected idea card")
    p_autodiscovery_reject.add_argument("--idea-bank", default=str(DEFAULT_IDEA_BANK))
    p_autodiscovery_reject.add_argument("--id", default=None, help="optional stable card id")
    p_autodiscovery_reject.add_argument("--title", required=True)
    p_autodiscovery_reject.add_argument("--package", default="")
    p_autodiscovery_reject.add_argument("--api-surface", default="")
    p_autodiscovery_reject.add_argument("--source", default="")
    p_autodiscovery_reject.add_argument("--tried-because", default="")
    p_autodiscovery_reject.add_argument("--rejected-because", action="append", default=[])
    p_autodiscovery_reject.add_argument("--future-avoid", default="")
    p_autodiscovery_reject.add_argument("--future-may-try", default="")
    p_autodiscovery_reject.set_defaults(func=cmd_autodiscovery_reject)

    p_autodiscovery_accept = autodiscovery_sub.add_parser("accept", help="append an accepted case anchor")
    p_autodiscovery_accept.add_argument("--idea-bank", default=str(DEFAULT_IDEA_BANK))
    p_autodiscovery_accept.add_argument("--id", default=None, help="optional stable card id")
    p_autodiscovery_accept.add_argument("--case-id", required=True)
    p_autodiscovery_accept.add_argument("--package", default="")
    p_autodiscovery_accept.add_argument("--api-surface", default="")
    p_autodiscovery_accept.add_argument("--versions", default="")
    p_autodiscovery_accept.add_argument("--source", default="")
    p_autodiscovery_accept.add_argument("--reproduction-path", default="")
    p_autodiscovery_accept.add_argument("--oracle-path", default="")
    p_autodiscovery_accept.add_argument("--package-path", default="")
    p_autodiscovery_accept.add_argument("--audit-path", default="")
    p_autodiscovery_accept.add_argument("--why-non-duplicate", default="")
    p_autodiscovery_accept.add_argument("--follow-up-idea", action="append", default=[])
    p_autodiscovery_accept.set_defaults(func=cmd_autodiscovery_accept)

    p_autodiscovery_log = autodiscovery_sub.add_parser("log", help="append a batch-level run note")
    p_autodiscovery_log.add_argument("--run-log", default=str(DEFAULT_RUN_LOG))
    p_autodiscovery_log.add_argument("--title", required=True)
    p_autodiscovery_log.add_argument("--model-or-operator", default="")
    p_autodiscovery_log.add_argument("--search-budget", default="")
    p_autodiscovery_log.add_argument("--package-searched", action="append", default=[])
    p_autodiscovery_log.add_argument("--idea-added", action="append", default=[])
    p_autodiscovery_log.add_argument("--idea-rejected", action="append", default=[])
    p_autodiscovery_log.add_argument("--promoted", action="append", default=[])
    p_autodiscovery_log.add_argument("--accepted", action="append", default=[])
    p_autodiscovery_log.add_argument("--note", action="append", default=[])
    p_autodiscovery_log.set_defaults(func=cmd_autodiscovery_log)

    p_autodiscovery_avoid = autodiscovery_sub.add_parser(
        "avoid-list",
        help="summarize packages, APIs, accepted anchors, and rejection lessons from the idea bank",
    )
    p_autodiscovery_avoid.add_argument("--idea-bank", default=str(DEFAULT_IDEA_BANK))
    p_autodiscovery_avoid.add_argument("--out", default=None)
    p_autodiscovery_avoid.set_defaults(func=cmd_autodiscovery_avoid)

    p_autodiscovery_readiness = autodiscovery_sub.add_parser(
        "readiness",
        help="check Markdown memory files and summarize whether discovery can be started",
    )
    p_autodiscovery_readiness.add_argument("--idea-bank", default=str(DEFAULT_IDEA_BANK))
    p_autodiscovery_readiness.add_argument("--run-log", default=str(DEFAULT_RUN_LOG))
    p_autodiscovery_readiness.add_argument("--plan", default=str(DEFAULT_PLAN))
    p_autodiscovery_readiness.add_argument("--run-brief", default=str(DEFAULT_RUN_BRIEF))
    p_autodiscovery_readiness.add_argument("--out", default=None)
    p_autodiscovery_readiness.set_defaults(func=cmd_autodiscovery_readiness)

    p_autodiscovery_brief = autodiscovery_sub.add_parser(
        "brief",
        help="write a model-readable next-run brief without starting discovery",
    )
    p_autodiscovery_brief.add_argument("--idea-bank", default=str(DEFAULT_IDEA_BANK))
    p_autodiscovery_brief.add_argument("--run-log", default=str(DEFAULT_RUN_LOG))
    p_autodiscovery_brief.add_argument("--attempts", type=int, default=10)
    p_autodiscovery_brief.add_argument("--package-focus", action="append", default=[])
    p_autodiscovery_brief.add_argument("--out", default=str(DEFAULT_RUN_BRIEF))
    p_autodiscovery_brief.set_defaults(func=cmd_autodiscovery_brief)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
