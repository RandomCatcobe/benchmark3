# typer_optional_list_none_default

Real Python silent-drift candidate for Typer command parameters typed as
`Optional[List[str]] = None`.

Source: https://typer.tiangolo.com/release-notes/

Typer 0.10.0 fixes a default-value case for optional list parameters. The
hand-authored client builds a local Typer app, invokes it with `CliRunner`, and
prints the value received by the callback. No shell process, live terminal,
network, clock, or random input is involved.

Run the local verification with:

```powershell
$env:PYTHONPATH='silent_drift_miner\src'
.\.uv-python\cpython-3.10.20-windows-x86_64-none\python.exe -m silent_drift_miner.cli reproduce run --spec data\verification\python_typer_optional_list_none_default\spec.json --out data\verification\python_typer_optional_list_none_default --install --venv-root .repro_venvs --timeout 60 --build-timeout 300
```

Expected observation:

- `typer==0.9.4`: callback receives `[]`.
- `typer==0.10.0`: callback receives `None`.
