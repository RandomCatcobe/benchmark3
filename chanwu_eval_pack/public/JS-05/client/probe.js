const mongoose = require("mongoose");
const schema = new mongoose.Schema({ known: Number });
const Model = mongoose.model("Probe" + process.version.replace(/\W/g, ""), schema);
const query = Model.find({ unknown: "x" });
query.cast(Model);
console.log(JSON.stringify({
  version: mongoose.version,
  strictQuery: mongoose.get("strictQuery"),
  filter: query.getFilter()
}));
