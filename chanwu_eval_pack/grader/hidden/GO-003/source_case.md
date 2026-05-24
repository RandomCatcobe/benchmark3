# GO-003: ServeMux treats method and brace patterns as structured routes

## API Or Behavior Under Test

net/http ServeMux matching for a pattern containing an HTTP method and a path variable.

## Version Boundary

Go 1.21.x -> Go 1.22+

## Old Behavior

The registered pattern is treated literally and the request falls through with an empty matched pattern.

## New Behavior

The pattern matches GET /posts/123 and returns GET /posts/{id}.

## Why The Drift Is Silent

The handler lookup returns a handler in both versions, but route identity changes.

## Realistic Impact Scenario

Metrics, auth, or request handling keyed by ServeMux pattern can silently attach to a different route.
