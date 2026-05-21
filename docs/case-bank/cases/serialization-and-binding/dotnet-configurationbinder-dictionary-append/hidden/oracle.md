# Oracle For DOTNET-05

Compare the old-version and new-version probe outputs after normalizing runtime log noise.

## Required Assertions

- dictionary collection binding preserves old item: `values.Key` old=['NewValue'] new=['InitialValue', 'NewValue']
