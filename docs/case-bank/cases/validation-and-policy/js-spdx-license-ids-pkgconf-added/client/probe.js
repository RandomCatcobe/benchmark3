const ids = require("spdx-license-ids");
console.log(JSON.stringify({ hasPkgconf: ids.includes("pkgconf"), count: ids.length }));
