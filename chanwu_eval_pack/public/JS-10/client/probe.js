const Handlebars = require("handlebars");
const proto = { inherited: "proto-value" };
const value = Object.create(proto);
const template = Handlebars.compile("{{inherited}}");
console.log(JSON.stringify({
  version: Handlebars.VERSION,
  rendered: template(value)
}));
