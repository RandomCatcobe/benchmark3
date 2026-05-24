# Environment For OLD15-003

## Inputs

- Reproduction result: data/verification/old_15/old15-httpx-json-request-body-compact/attempt_003/result.json
- Client source: cases/httpx_json_request_body_compact/client.py
- Old side: httpx 0.27.2
- New side: httpx 0.28.0

## Command Shape

Rerun with: `silent-drift-miner reproduce run --spec data/verification/old_15/old15-httpx-json-request-body-compact/attempt_003/spec.json --out <attempt-root>`

- Client file in spec: `cases\httpx_json_request_body_compact\client.py`
- Old install command: `python -m pip install httpx==0.27.2`
- New install command: `python -m pip install httpx==0.28.0`

## Local Run Logs

- Old stdout: data/verification/old_15/old15-httpx-json-request-body-compact/attempt_003/old/stdout.txt
- Old stderr: data/verification/old_15/old15-httpx-json-request-body-compact/attempt_003/old/stderr.txt
- New stdout: data/verification/old_15/old15-httpx-json-request-body-compact/attempt_003/new/stdout.txt
- New stderr: data/verification/old_15/old15-httpx-json-request-body-compact/attempt_003/new/stderr.txt
