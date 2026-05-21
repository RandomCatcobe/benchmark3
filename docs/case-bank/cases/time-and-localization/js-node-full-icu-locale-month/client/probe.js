const date = new Date(Date.UTC(2020, 0, 1));
const month = new Intl.DateTimeFormat("es", { month: "long", timeZone: "UTC" }).format(date);
const supported = Intl.DateTimeFormat.supportedLocalesOf(["es", "fr", "zh-CN", "ar", "hi"]);
console.log(JSON.stringify({
  node: process.version,
  supported,
  month,
  supported_es: supported.includes("es")
}));
