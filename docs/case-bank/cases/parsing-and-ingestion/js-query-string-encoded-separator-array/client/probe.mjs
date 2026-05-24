import queryString from "query-string";
const parsed = queryString.parse("ids=1%7C2", { arrayFormat: "separator", arrayFormatSeparator: "|" });
console.log(JSON.stringify({ ids: parsed.ids, isArray: Array.isArray(parsed.ids) }));
