const setCookie = require("set-cookie-parser");
const parsed = setCookie.parse("sid=abc; Secure; SameSite=None; Partitioned")[0];
console.log(JSON.stringify({
  partitioned: parsed.partitioned === true,
  secure: parsed.secure === true,
  sameSite: parsed.sameSite || parsed.samesite || null
}));
