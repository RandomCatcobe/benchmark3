# RB-RACK-006: Rack Response normalizes response header names to lowercase

## API Or Behavior Under Test

Header keys stored by Rack::Response.

## Version Boundary

Rack 2.2.9 -> Rack 3.1.0

## Old Behavior

Header keys preserve Content-Type and X-Test casing.

## New Behavior

Header keys are normalized to content-type and x-test.

## Why The Drift Is Silent

Response construction succeeds and header values are still present.

## Realistic Impact Scenario

Middleware or tests that look up headers by raw key casing can silently stop matching.
