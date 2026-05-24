# RB-STRICT-001: public_suffix recognizes pages.gay as a public suffix

## API Or Behavior Under Test

`PublicSuffix.domain` from the Ruby `public_suffix` gem.

## Version Boundary

`public_suffix` 5.0.4 -> 5.0.5.

## Old Behavior

`PublicSuffix.domain("foo.pages.gay")` returns `pages.gay`.

## New Behavior

The same call returns `foo.pages.gay`.

## Why The Drift Is Silent

The API returns normally in both versions with empty stderr. Only the built-in public suffix data changes the parsed registrable domain.

## Realistic Impact Scenario

Tenant routing, cookie scoping, or domain ownership checks can silently classify the same hostname differently after a patch update.
