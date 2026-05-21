# DOTNET-05: ConfigurationBinder appends dictionary collection values

## API Or Behavior Under Test

Binding configuration into an existing dictionary whose value is a collection.

## Version Boundary

Microsoft.Extensions.Configuration.Binder 6.x -> Microsoft.Extensions.Configuration.Binder 7.x

## Old Behavior

The binder replaces the existing collection with the configured value.

## New Behavior

The binder extends the existing collection and preserves the prior value.

## Why The Drift Is Silent

The bind call succeeds in both versions and returns the same object type.

## Realistic Impact Scenario

A service can keep stale configured values after an upgrade, changing effective routing, allowlists, or feature flags.
