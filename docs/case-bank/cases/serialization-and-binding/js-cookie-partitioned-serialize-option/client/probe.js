const cookie = require("cookie");
const text = cookie.serialize("sid", "abc", { partitioned: true, secure: true, sameSite: "none" });
console.log(JSON.stringify({ text, hasPartitioned: text.includes("Partitioned") }));
