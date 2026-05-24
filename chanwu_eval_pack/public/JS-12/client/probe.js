const { parseDocument } = require("htmlparser2");
const textarea = parseDocument("<textarea><b>x</b></textarea>").children[0];
const child = textarea.children[0];
console.log(JSON.stringify({
  childType: child.type,
  childName: child.name || null,
  childData: child.data || null
}));
