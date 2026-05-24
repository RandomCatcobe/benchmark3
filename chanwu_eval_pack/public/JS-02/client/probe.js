const fs = require("fs");
const lock = JSON.parse(fs.readFileSync("package-lock.json", "utf8"));
console.log(JSON.stringify({ lockfileVersion: lock.lockfileVersion }));
