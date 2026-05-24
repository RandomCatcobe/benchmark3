const semver = require("semver");
const version = semver.coerce("prefix 1.2.3-beta.4+build.5", { includePrerelease: true });
console.log(JSON.stringify({ version: version && version.version }));
