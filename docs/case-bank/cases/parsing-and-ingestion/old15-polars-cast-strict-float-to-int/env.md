# Environment For OLD15-011

## Inputs

- Reproduction result: data/verification/old_15/old15-polars-cast-strict-float-to-int/attempt_001/result.json
- Client source: cases/polars_cast_strict_float_to_int/client.py
- Old side: polars 1.0.0
- New side: polars 1.30.0

## Command Shape

Rerun with: `silent-drift-miner reproduce run --spec data/verification/old_15/old15-polars-cast-strict-float-to-int/attempt_001/spec.json --out <attempt-root>`

- Client file in spec: `cases\polars_cast_strict_float_to_int\client.py`
- Old install command: `python -m pip install polars==1.0.0`
- New install command: `python -m pip install polars==1.30.0`

## Local Run Logs

- Old stdout: data/verification/old_15/old15-polars-cast-strict-float-to-int/attempt_001/old/stdout.txt
- Old stderr: data/verification/old_15/old15-polars-cast-strict-float-to-int/attempt_001/old/stderr.txt
- New stdout: data/verification/old_15/old15-polars-cast-strict-float-to-int/attempt_001/new/stdout.txt
- New stderr: data/verification/old_15/old15-polars-cast-strict-float-to-int/attempt_001/new/stderr.txt
