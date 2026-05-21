# Oracle For GO-006

        Compare the old-version and new-version probe outputs after normalizing runtime log noise.

        ## Required Assertions

        - build output becomes structured: `has_build_output_event` old=False new=True
- failed build id appears: `failed_build` old='<missing>' new='go006'
