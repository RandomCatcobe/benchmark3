const fs = require("fs");
const prettier = require("prettier");

async function main() {
  const input = fs.readFileSync("input.js", "utf8");
  const formatted = await prettier.format(input, { parser: "babel", printWidth: 20 });
  console.log(JSON.stringify({
    formatted,
    trailing_call_comma: formatted.includes('"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",')
  }));
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
