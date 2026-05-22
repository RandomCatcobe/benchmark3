# Evidence For OLD15-015

## Sources

- https://scikit-learn.org/stable/whats_new/v1.2.html

## Source Excerpt Or Provenance Note

KMeans accepts n_init='auto', begins deprecation for default n_init, and defaults are changed to n_init='auto' in 1.4.

## Version Boundary

- Old version: 1.3.2
- New version: 1.5.2

## Replay Artifact

- Result: data/verification/old_15/old15-sklearn-kmeans-n-init-auto/attempt_001/result.json
- Status: verified_keep
- Diff summary: stdout changed, stderr changed
- First blocker: none

## Review Notes

Accepted as uncertain-silence: behavior reproduces as actual _n_init 10 versus 1, but sklearn 1.3.2 emits a FutureWarning and release notes announced the default shift.
