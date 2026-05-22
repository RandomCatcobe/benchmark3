# Environment For OLD15-008

## Inputs

- Reproduction result: data/verification/old_15/old15-pandas-str-replace-regex-default/attempt_001/result.json
- Client source: cases/pandas_str_replace_regex_default/client.py
- Old side: pandas 1.5.3
- New side: pandas 2.0.3

## Command Shape

Rerun with: `silent-drift-miner reproduce run --spec data/verification/old_15/old15-pandas-str-replace-regex-default/attempt_001/spec.json --out <attempt-root>`

- Client file in spec: `cases\pandas_str_replace_regex_default\client.py`
- Old install command: `python -m pip install numpy==1.24.4 pandas==1.5.3`
- New install command: `python -m pip install numpy==1.24.4 pandas==2.0.3`

## Local Run Logs

- Old stdout: data/verification/old_15/old15-pandas-str-replace-regex-default/attempt_001/old/stdout.txt
- Old stderr: data/verification/old_15/old15-pandas-str-replace-regex-default/attempt_001/old/stderr.txt
- New stdout: data/verification/old_15/old15-pandas-str-replace-regex-default/attempt_001/new/stdout.txt
- New stderr: data/verification/old_15/old15-pandas-str-replace-regex-default/attempt_001/new/stderr.txt
