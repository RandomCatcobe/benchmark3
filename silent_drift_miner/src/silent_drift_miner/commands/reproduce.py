"""Reproduction command implementations."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .common import artifact_path
from ..adapter_contracts import AdapterPlanRequest, AdapterRunRequest
from ..adapters.registry import adapter_for_spec_payload, get_adapter, get_registered_adapter
from ..client_generation import write_client_generation_artifacts
from ..reproduction import (
    create_reproduction_spec,
    load_reproduction_result,
    load_reproduction_spec,
    run_reproduction_spec,
    write_reproduction_spec,
)


def cmd_reproduce_plan(args: argparse.Namespace) -> int:
    client_file = Path(args.client_file)
    if not client_file.exists():
        print(f"client file not found: {client_file}", file=sys.stderr)
        return 2

    out_path = artifact_path(args.out, args.artifact_root)
    ecosystem = getattr(args, "ecosystem", "python").lower()
    if ecosystem == "jvm":
        if not args.old_source_path or not args.new_source_path:
            print("ERROR JVM reproduction requires --old-source-path and --new-source-path", file=sys.stderr)
            return 2
        metadata = {
            "old_source_paths": args.old_source_path,
            "new_source_paths": args.new_source_path,
            "classpath": args.classpath,
            "old_classpath": args.old_classpath,
            "new_classpath": args.new_classpath,
            "resource_paths": args.resource_path,
            "old_resource_paths": args.old_resource_path,
            "new_resource_paths": args.new_resource_path,
            "jvm_args": args.jvm_arg,
            "old_jvm_args": args.old_jvm_arg,
            "new_jvm_args": args.new_jvm_arg,
            "program_args": args.program_arg,
            "old_program_args": args.old_program_arg,
            "new_program_args": args.new_program_arg,
            "main_class": args.main_class,
            "java_executable": args.java_executable,
            "javac_executable": args.javac_executable,
        }
        return _plan_registered_adapter(args, "jvm", client_file, out_path, metadata)
    if ecosystem == "js":
        if not args.old_package_path or not args.new_package_path:
            print("ERROR JS reproduction requires --old-package-path and --new-package-path", file=sys.stderr)
            return 2
        metadata = {
            "old_package_path": args.old_package_path,
            "new_package_path": args.new_package_path,
            "module_paths": args.module_path,
            "old_module_paths": args.old_module_path,
            "new_module_paths": args.new_module_path,
            "node_args": args.node_arg,
            "old_node_args": args.old_node_arg,
            "new_node_args": args.new_node_arg,
            "program_args": args.program_arg,
            "old_program_args": args.old_program_arg,
            "new_program_args": args.new_program_arg,
            "node_executable": args.node_executable,
        }
        return _plan_registered_adapter(args, "js", client_file, out_path, metadata)
    if ecosystem == "php":
        if not args.old_package_path or not args.new_package_path:
            print("ERROR PHP reproduction requires --old-package-path and --new-package-path", file=sys.stderr)
            return 2
        metadata = {
            "old_package_path": args.old_package_path,
            "new_package_path": args.new_package_path,
            "include_paths": args.include_path,
            "old_include_paths": args.old_include_path,
            "new_include_paths": args.new_include_path,
            "php_args": args.php_arg,
            "old_php_args": args.old_php_arg,
            "new_php_args": args.new_php_arg,
            "program_args": args.program_arg,
            "old_program_args": args.old_program_arg,
            "new_program_args": args.new_program_arg,
            "php_executable": args.php_executable,
            "old_php_executable": args.old_php_executable,
            "new_php_executable": args.new_php_executable,
        }
        return _plan_registered_adapter(args, "php", client_file, out_path, metadata)
    if ecosystem == "ruby":
        if not args.old_package_path or not args.new_package_path:
            print("ERROR Ruby reproduction requires --old-package-path and --new-package-path", file=sys.stderr)
            return 2
        metadata = {
            "old_package_path": args.old_package_path,
            "new_package_path": args.new_package_path,
            "load_paths": args.load_path,
            "old_load_paths": args.old_load_path,
            "new_load_paths": args.new_load_path,
            "ruby_args": args.ruby_arg,
            "old_ruby_args": args.old_ruby_arg,
            "new_ruby_args": args.new_ruby_arg,
            "program_args": args.program_arg,
            "old_program_args": args.old_program_arg,
            "new_program_args": args.new_program_arg,
            "ruby_executable": args.ruby_executable,
        }
        return _plan_registered_adapter(args, "ruby", client_file, out_path, metadata)
    if ecosystem == "dotnet":
        if not args.old_package_path or not args.new_package_path:
            print("ERROR .NET reproduction requires --old-package-path and --new-package-path", file=sys.stderr)
            return 2
        metadata = {
            "old_package_path": args.old_package_path,
            "new_package_path": args.new_package_path,
            "reference_paths": args.reference_path,
            "old_reference_paths": args.old_reference_path,
            "new_reference_paths": args.new_reference_path,
            "dotnet_args": args.dotnet_arg,
            "old_dotnet_args": args.old_dotnet_arg,
            "new_dotnet_args": args.new_dotnet_arg,
            "program_args": args.program_arg,
            "old_program_args": args.old_program_arg,
            "new_program_args": args.new_program_arg,
            "dotnet_executable": args.dotnet_executable,
            "no_restore": not args.dotnet_restore,
        }
        return _plan_registered_adapter(args, "dotnet", client_file, out_path, metadata)
    if ecosystem == "go":
        if not args.old_package_path or not args.new_package_path:
            print("ERROR Go reproduction requires --old-package-path and --new-package-path", file=sys.stderr)
            return 2
        metadata = {
            "old_package_path": args.old_package_path,
            "new_package_path": args.new_package_path,
            "module_paths": args.go_module_path,
            "old_module_paths": args.old_go_module_path,
            "new_module_paths": args.new_go_module_path,
            "go_args": args.go_arg,
            "old_go_args": args.old_go_arg,
            "new_go_args": args.new_go_arg,
            "program_args": args.program_arg,
            "old_program_args": args.old_program_arg,
            "new_program_args": args.new_program_arg,
            "go_executable": args.go_executable,
            "no_network": not args.go_network,
        }
        return _plan_registered_adapter(args, "go", client_file, out_path, metadata)
    if ecosystem != "python":
        print(f"ERROR unsupported reproduction ecosystem: {args.ecosystem}", file=sys.stderr)
        return 2

    spec = create_reproduction_spec(
        candidate_id=args.candidate_id,
        library=args.library,
        old_version=args.old_version,
        new_version=args.new_version,
        client_file=client_file,
        old_package_path=args.old_package_path,
        new_package_path=args.new_package_path,
        old_python_executable=args.old_python_executable,
        new_python_executable=args.new_python_executable,
        extra_packages=args.extra_package,
        old_extra_packages=args.old_extra_package,
        new_extra_packages=args.new_extra_package,
        ignore_json_fields=args.ignore_json_field,
    )
    write_reproduction_spec(spec, out_path)
    print(f"wrote reproduction spec -> {out_path}")
    return 0


def cmd_reproduce_run(args: argparse.Namespace) -> int:
    spec_path = artifact_path(args.spec, args.artifact_root)
    out_path = artifact_path(args.out, args.artifact_root)
    try:
        spec_payload = json.loads(spec_path.read_text(encoding="utf-8"))
        adapter = adapter_for_spec_payload(spec_payload)
        if adapter:
            metadata = {}
            if spec_payload.get("ecosystem") == "jvm":
                metadata["build_timeout_s"] = args.build_timeout
            result_path = adapter.run(
                AdapterRunRequest(
                    spec_path=str(spec_path),
                    out_dir=str(out_path),
                    timeout_s=args.timeout,
                    metadata=metadata,
                )
            )
            result = load_reproduction_result(result_path)
        else:
            spec = load_reproduction_spec(spec_path)
            venv_root = Path(args.venv_root) if args.venv_root else None
            result = run_reproduction_spec(
                spec,
                out_path,
                timeout_s=args.timeout,
                install=args.install,
                venv_root=venv_root,
                build_timeout_s=args.build_timeout,
            )
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    print(f"wrote reproduction result -> {Path(result.attempt_dir) / 'result.json'}")
    print(json.dumps({
        "keep": result.keep,
        "drop_reason": result.drop_reason.value if result.drop_reason else None,
        "summary": result.diff.summary,
    }, ensure_ascii=False))
    return 0


def cmd_reproduce_summarize(args: argparse.Namespace) -> int:
    result_path = artifact_path(args.result, args.artifact_root)
    try:
        result = load_reproduction_result(result_path)
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    print(json.dumps({
        "candidate_id": result.candidate_id,
        "attempt_dir": result.attempt_dir,
        "keep": result.keep,
        "drop_reason": result.drop_reason.value if result.drop_reason else None,
        "diff_summary": result.diff.summary,
    }, indent=2, ensure_ascii=False))
    return 0


def cmd_reproduce_generate_client(args: argparse.Namespace) -> int:
    candidate_path = artifact_path(args.candidate, args.artifact_root)
    out_path = artifact_path(args.out, args.artifact_root)
    prompt_out = artifact_path(args.prompt_out, args.artifact_root) if args.prompt_out else None
    metadata_out = artifact_path(args.metadata_out, args.artifact_root) if args.metadata_out else None
    try:
        artifacts = write_client_generation_artifacts(
            candidate_path=candidate_path,
            candidate_id=args.candidate_id,
            out_path=out_path,
            redacted=args.redacted,
            dry_run=args.dry_run,
            model=args.model,
            provider=args.provider,
            allowed_imports=args.allowed_import,
            forbidden_terms=args.forbidden_term,
            prompt_out=prompt_out,
            metadata_out=metadata_out,
        )
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    print(artifacts.to_json())
    return 0


def _plan_registered_adapter(
    args: argparse.Namespace,
    ecosystem: str,
    client_file: Path,
    out_path: Path,
    metadata: dict,
) -> int:
    try:
        get_adapter(ecosystem).plan(
            AdapterPlanRequest(
                candidate_id=args.candidate_id,
                ecosystem=ecosystem,
                library=args.library,
                old_version=args.old_version,
                new_version=args.new_version,
                client_file=str(client_file),
                out_path=str(out_path),
                metadata=metadata,
            )
        )
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    print(f"wrote {get_registered_adapter(ecosystem).display_name} reproduction spec -> {out_path}")
    return 0
