# Environment For JS-01

        - Old version: Node.js 12.22.12 small-ICU.
        - New version: Node.js 13.14.0 full-ICU.
        - Adapter/API surface: runtime-api, intl.
        - Runtime: Node.js pair with old small-ICU and new full-ICU builds.
- Version switching: run node client/probe.js under both runtimes.
- Probe shape: parse one JSON object from stdout.
