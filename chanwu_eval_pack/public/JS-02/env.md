# Environment For JS-02

        - Old version: npm 6.x.
        - New version: npm 7.x.
        - Adapter/API surface: package-manager, lockfile.
        - Runtime: Node.js with npm 6.x and npm 7.x available.
- Version switching: remove package-lock.json, run npm install --package-lock-only, then run node probe.js.
- Probe shape: parse package-lock.json and report lockfileVersion.
