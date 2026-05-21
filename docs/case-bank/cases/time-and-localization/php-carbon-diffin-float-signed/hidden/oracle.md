# Oracle For PHP-08

        Compare the old-version and new-version probe outputs after normalizing runtime log noise.

        ## Required Assertions

        - forward diff precision changes: `forward` old=0 new=0.5
- reverse diff sign changes: `reverse` old=0 new=-0.5
- return type changes: `forward_type` old='integer' new='double'
