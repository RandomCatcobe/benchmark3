# PHP-03: PHP core htmlspecialchars(), htmlentities() defaults

## Migration Status

The 2026-05-21 verification pass did not promote this as an independent silent drift. It is retained as a rejected or duplicate migration record from the requested 30+50 scope.

Original run status: `skipped_existing_record`.
First blocked step: `none recorded`.

## Behavior Under Review

Default flags changed from `ENT_COMPAT` to `ENT_QUOTES | ENT_SUBSTITUTE`, so single quotes and malformed UTF-8 encode differently.

Version boundary: `PHP 8.0` -> `8.1`.

## Why It Matters

Same call with omitted flags succeeds; escaped text changes.

## Current Package Role

This folder migrates the 30+50 verification record into the case bank without claiming a successful silent-drift reproduction. Other agents can independently retry the reproduction from this package and the linked source notes.
