# Evidence For PY-HOL-020

## Sources

- https://github.com/vacanza/holidays/releases/tag/v0.29

## Source Excerpt Or Provenance Note

The holidays release updates bundled country holiday definitions while preserving the country_holidays API.

## Version Boundary

- Old version: 0.28
- New version: 0.29

## Replay Artifact

- Result: data/verification/strict_python_holidays/python-holidays-td-eid-estimate-marker/attempt_001/result.json
- Status: rejected_cluster_duplicate
- Diff summary: stdout changed
- First blocker: none

## Review Notes

Clean old/new reproduction with stdout drift, but rejected during curation because the holidays cluster is already represented by PY-HOL-015, PY-HOL-026, and PY-HOL-036. Keeping more same-upstream bundled-calendar data slices would overweight one package and weaken benchmark diversity.
