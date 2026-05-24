const validator = require("validator");
console.log(JSON.stringify({
  port01: validator.isPort("01"),
  port00080: validator.isPort("00080"),
  port80: validator.isPort("80")
}));
