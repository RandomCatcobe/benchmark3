# JVM-JAVA-11: jsoup Element.text inserts spacing between block and inline elements

## API Or Behavior Under Test

`Jsoup.parse(...).text()` from `org.jsoup:jsoup`.

## Version Boundary

`org.jsoup:jsoup` 1.15.3 -> 1.15.4.

## Old Behavior

Parsing `<div>One</div><span>Two</span>` and reading `text()` returns `OneTwo`.

## New Behavior

The same call returns `One Two`.

## Why The Drift Is Silent

The parser call and text accessor succeed in both versions with empty stderr. Only the returned text content changes.

## Realistic Impact Scenario

HTML ingestion code that extracts plain text for search, deduplication, or moderation can silently produce different tokens after a patch update.
