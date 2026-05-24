# Environment For OLD15-009

## Inputs

- Reproduction result: data/verification/old_15/old15-pandas-timestamp-to-datetime64-resolution/attempt_003/result.json
- Client source: cases/pandas_timestamp_to_datetime64_resolution/client.py
- Old side: pandas 1.5.3
- New side: pandas 2.0.3

## Command Shape

Rerun with: `silent-drift-miner reproduce run --spec data/verification/old_15/old15-pandas-timestamp-to-datetime64-resolution/attempt_003/spec.json --out <attempt-root>`

- Client file in spec: `cases\pandas_timestamp_to_datetime64_resolution\client.py`
- Old install command: `python -m pip install numpy==1.24.4 pandas==1.5.3`
- New install command: `python -m pip install numpy==1.24.4 pandas==2.0.3`

## Local Run Logs

- Old stdout: data/verification/old_15/old15-pandas-timestamp-to-datetime64-resolution/attempt_003/old/stdout.txt
- Old stderr: data/verification/old_15/old15-pandas-timestamp-to-datetime64-resolution/attempt_003/old/stderr.txt
- New stdout: data/verification/old_15/old15-pandas-timestamp-to-datetime64-resolution/attempt_003/new/stdout.txt
- New stderr: data/verification/old_15/old15-pandas-timestamp-to-datetime64-resolution/attempt_003/new/stderr.txt
