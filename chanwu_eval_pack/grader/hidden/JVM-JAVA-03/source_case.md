# JVM-JAVA-03: Hibernate native count result changes from BigInteger to Long

## API Or Behavior Under Test

Type returned by a native SQL count expression.

## Version Boundary

Hibernate ORM 5.6.15.Final -> Hibernate ORM 6.0.0.Final

## Old Behavior

The result object is java.math.BigInteger:35.

## New Behavior

The result object is java.lang.Long:35.

## Why The Drift Is Silent

The query succeeds and the numeric value is the same.

## Realistic Impact Scenario

Code that branches on result type or casts native query counts can silently break later in the flow.
