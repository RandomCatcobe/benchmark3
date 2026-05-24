# Environment For PY-STRICT-018

## Inputs

- Reproduction result: data/verification/strict_python_new/python-urllib3-httpconnection-blocksize-default/attempt_001/result.json
- Client source: data/verification/strict_python_new/python-urllib3-httpconnection-blocksize-default/client.py
- Old side: urllib3 2.0.4
- New side: urllib3 2.0.5

## Command Shape

Rerun with: `silent-drift-miner reproduce run --spec data/verification/strict_python_new/python-urllib3-httpconnection-blocksize-default/attempt_001/spec.json --out <attempt-root>`

- Client file in spec: `D:\myproject\bench2\shishan\worktree\beachmark4silentdrift\data\verification\strict_python_new\python-urllib3-httpconnection-blocksize-default\client.py`
- Old install command: `python -m pip install urllib3==2.0.4`
- New install command: `python -m pip install urllib3==2.0.5`

## Local Run Logs

- Old stdout: data/verification/strict_python_new/python-urllib3-httpconnection-blocksize-default/attempt_001/old/stdout.txt
- Old stderr: data/verification/strict_python_new/python-urllib3-httpconnection-blocksize-default/attempt_001/old/stderr.txt
- New stdout: data/verification/strict_python_new/python-urllib3-httpconnection-blocksize-default/attempt_001/new/stdout.txt
- New stderr: data/verification/strict_python_new/python-urllib3-httpconnection-blocksize-default/attempt_001/new/stderr.txt
