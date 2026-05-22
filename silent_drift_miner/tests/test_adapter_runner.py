from __future__ import annotations

import sys

from silent_drift_miner.adapters.common.runner import run_command


def test_run_command_captures_stdout_stderr_and_exit_code() -> None:
    result = run_command(
        [
            sys.executable,
            "-c",
            "import sys; print('out'); print('err', file=sys.stderr); sys.exit(3)",
        ],
        timeout_s=10,
    )

    assert result == {"stdout": "out\n", "stderr": "err\n", "exit_code": 3}


def test_run_command_classifies_missing_tool_like_adapters_expect() -> None:
    result = run_command(["definitely-missing-adapter-tool"], timeout_s=10)

    assert result["stdout"] == ""
    assert result["exit_code"] == 127
    assert "definitely-missing-adapter-tool" in result["stderr"]
