# GO-005: mime/multipart (*multipart.Part).FileName()

## Migration Status

The 2026-05-21 verification pass stopped at dependency or package acquisition. It is retained as a blocked-dependency migration record.

Original run status: `blocked`.
First blocked step: `dependency_acquired`.

## Behavior Under Review

Multipart filenames are now passed through `filepath.Base`; path-like uploaded filenames lose directory components.

Version boundary: `Go <1.17` -> `Go >=1.17`.

## Why It Matters

Multipart parsing succeeds; downstream code sees a different filename string.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
