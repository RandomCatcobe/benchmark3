const { URL } = require("whatwg-url");
const url = new URL("https://example.test/a^b?x=1^2");
console.log(JSON.stringify({ href: url.href, pathname: url.pathname, search: url.search }));
