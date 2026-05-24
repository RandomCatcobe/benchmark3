# Oracle For RB-STRICT-002

Run the probe against `mime-types-data 3.2025.0924` and `3.2026.0317`.

The old run must produce `{"content_type":"application/x-parquet"}` with exit code 0 and empty stderr.

The new run must produce `{"content_type":"application/vnd.apache.parquet"}` with exit code 0 and empty stderr.
