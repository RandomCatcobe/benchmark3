# JVM-JAVA-04: Spring Boot defaults to PathPatternParser matching

## API Or Behavior Under Test

Default Spring MVC path matching strategy.

## Version Boundary

Spring Boot 2.5.x -> Spring Boot 2.6.x

## Old Behavior

The default strategy is ANT_PATH_MATCHER.

## New Behavior

The default strategy is PATH_PATTERN_PARSER.

## Why The Drift Is Silent

The application context can start successfully in both versions.

## Realistic Impact Scenario

Route matching, interceptors, or path-variable behavior can change without explicit configuration.
