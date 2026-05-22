"""Shared subprocess runner for ecosystem adapters."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Mapping


def run_command(
    command: list[str],
    timeout_s: int,
    *,
    env: Mapping[str, str] | None = None,
    cwd: Path | None = None,
) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            env=dict(env) if env is not None else None,
            cwd=cwd,
            check=False,
        )
        return {"stdout": completed.stdout, "stderr": completed.stderr, "exit_code": completed.returncode}
    except FileNotFoundError as exc:
        executable = command[0] if command else "<empty command>"
        return {"stdout": "", "stderr": f"{executable}: {exc}\n", "exit_code": 127}
    except subprocess.TimeoutExpired as exc:
        return {
            "stdout": exc.stdout or "",
            "stderr": (exc.stderr or "") + f"\nTIMEOUT after {timeout_s}s\n",
            "exit_code": 124,
        }
