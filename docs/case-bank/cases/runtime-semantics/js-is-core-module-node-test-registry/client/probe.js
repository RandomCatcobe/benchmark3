const isCore = require("is-core-module");
console.log(JSON.stringify({
  nodeTest18: isCore("node:test", "18.0.0"),
  nodeTest16: isCore("node:test", "16.0.0")
}));
