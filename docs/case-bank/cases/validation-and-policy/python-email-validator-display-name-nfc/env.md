# Environment For PY-STRICT-019

## Inputs

- Reproduction result: data/verification/strict_python_new/python-email-validator-display-name-nfc/attempt_001/result.json
- Client source: data/verification/strict_python_new/python-email-validator-display-name-nfc/client.py
- Old side: email-validator 2.2.0
- New side: email-validator 2.3.0

## Command Shape

Rerun with: `silent-drift-miner reproduce run --spec data/verification/strict_python_new/python-email-validator-display-name-nfc/attempt_001/spec.json --out <attempt-root>`

- Client file in spec: `D:\myproject\bench2\shishan\worktree\beachmark4silentdrift\data\verification\strict_python_new\python-email-validator-display-name-nfc\client.py`
- Old install command: `python -m pip install email-validator==2.2.0`
- New install command: `python -m pip install email-validator==2.3.0`

## Local Run Logs

- Old stdout: data/verification/strict_python_new/python-email-validator-display-name-nfc/attempt_001/old/stdout.txt
- Old stderr: data/verification/strict_python_new/python-email-validator-display-name-nfc/attempt_001/old/stderr.txt
- New stdout: data/verification/strict_python_new/python-email-validator-display-name-nfc/attempt_001/new/stdout.txt
- New stderr: data/verification/strict_python_new/python-email-validator-display-name-nfc/attempt_001/new/stderr.txt
