# Oracle For GO-007

        Compare the old-version and new-version probe outputs after normalizing runtime log noise.

        ## Required Assertions

        - on scalar type changes: `flag.type` old='bool' new='string'
- no scalar type changes: `nope.type` old='bool' new='string'
