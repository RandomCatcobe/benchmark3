# Environment For OLD15-012

## Inputs

- Reproduction result: data/verification/old_15/old15-pydantic-field-alias-none/attempt_001/result.json
- Client source: cases/pydantic_field_alias_none/client.py
- Old side: pydantic 1.10.15
- New side: pydantic 2.7.4

## Command Shape

Rerun with: `silent-drift-miner reproduce run --spec data/verification/old_15/old15-pydantic-field-alias-none/attempt_001/spec.json --out <attempt-root>`

- Client file in spec: `cases\pydantic_field_alias_none\client.py`
- Old install command: `python -m pip install pydantic==1.10.15`
- New install command: `python -m pip install pydantic==2.7.4`

## Local Run Logs

- Old stdout: data/verification/old_15/old15-pydantic-field-alias-none/attempt_001/old/stdout.txt
- Old stderr: data/verification/old_15/old15-pydantic-field-alias-none/attempt_001/old/stderr.txt
- New stdout: data/verification/old_15/old15-pydantic-field-alias-none/attempt_001/new/stdout.txt
- New stderr: data/verification/old_15/old15-pydantic-field-alias-none/attempt_001/new/stderr.txt
