# Run Note: python-typer-optional-list-none-default

- Source idea: `IDEA-20260522-052`
- Ecosystem: python
- Adapter: python package install replay
- Library: typer
- Versions: `0.9.4 -> 0.10.0`
- Client: `cases/typer_optional_list_none_default/client.py`
- Local old/new roots: none; install from package cache/index into isolated venvs.
- Python executable: `.uv-python/cpython-3.10.20-windows-x86_64-none/python.exe`
- Extra package pin: `click==8.1.7`
- Expected command shape: plan with `--library typer --extra-package click==8.1.7`; run with `--install --venv-root .repro_venvs --timeout 60`.
- Expected observation: invoking the command with no repeated list argument passes `[]` to the callback in old Typer and `None` in new Typer.
