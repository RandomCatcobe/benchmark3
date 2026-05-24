# Evidence For RB-STRICT-002

## Source URLs

- https://github.com/mime-types/mime-types-data/blob/main/CHANGELOG.md

## Source Notes

The mime-types-data gem supplies the MIME registry used by mime-types; the local probe shows the Parquet content type update.

## Local Reproduction

- Old: `mime-types-data 3.2025.0924`
- New: `mime-types-data 3.2026.0317`
- Old stdout: `{"content_type":"application/x-parquet"}`
- New stdout: `{"content_type":"application/vnd.apache.parquet"}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/ruby_new_probe/ruby-mime-types-data-parquet-type`
