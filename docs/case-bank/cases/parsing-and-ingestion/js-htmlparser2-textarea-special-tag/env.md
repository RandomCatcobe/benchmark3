# Environment For JS-12

- Runtime: Node.js with npm package installation enabled.
- Package versions: `htmlparser2 9.0.0` and `htmlparser2 9.1.0`.
- Version switching: edit `client/package.json` to pin the target package version, then run `npm install`.
- Adapter/API surface: library-api.
- Probe shape: run the copied Node probe and parse one JSON object from stdout.
- Command shape: `npm install --silent --no-audit --fund=false`, then `npm run probe --silent`.
