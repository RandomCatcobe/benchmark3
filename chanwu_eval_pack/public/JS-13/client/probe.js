const AjvJTD = require("ajv/dist/jtd").default;
const ajv = new AjvJTD();
const serialize = ajv.compileSerializer({
  optionalProperties: {
    a: { type: "int32" },
    b: { type: "int32" }
  }
});
console.log(JSON.stringify({ serialized: serialize({ b: 1 }) }));
