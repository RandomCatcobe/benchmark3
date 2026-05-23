# Environment For PY-STRICT-001

## Inputs

- Reproduction result: data/verification/python_typer_optional_list_none_default/attempt_001/result.json
- Client source: cases/typer_optional_list_none_default/client.py
- Old side: typer 0.9.4
- New side: typer 0.10.0

## Command Shape

Rerun with: `silent-drift-miner reproduce run --spec data/verification/python_typer_optional_list_none_default/attempt_001/spec.json --out <attempt-root>`

- Client file in spec: `cases\typer_optional_list_none_default\client.py`
- Old install command: `python -m pip install click==8.1.7 typer==0.9.4`
- New install command: `python -m pip install click==8.1.7 typer==0.10.0`

## Local Run Logs

- Old stdout: data/verification/python_typer_optional_list_none_default/attempt_001/old/stdout.txt
- Old stderr: data/verification/python_typer_optional_list_none_default/attempt_001/old/stderr.txt
- New stdout: data/verification/python_typer_optional_list_none_default/attempt_001/new/stdout.txt
- New stderr: data/verification/python_typer_optional_list_none_default/attempt_001/new/stderr.txt
