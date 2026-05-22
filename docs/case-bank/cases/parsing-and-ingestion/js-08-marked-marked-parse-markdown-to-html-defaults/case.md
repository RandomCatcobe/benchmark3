# JS-08: Marked marked.parse markdown-to-HTML defaults

## Migration Status

The 2026-05-21 verification pass did not promote this as an independent silent drift. It is retained as a rejected or duplicate migration record from the requested 30+50 scope.

Original run status: `no_behavior_diff`.
First blocked step: `output_assertion`.

## Behavior Under Review

Built-in heading IDs and email mangling options were removed; default HTML for headings/mail links can change.

Version boundary: `Marked 7` -> `8`.

## Why It Matters

`marked.parse()` succeeds; generated HTML loses attributes or escaping unless extensions are added.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
