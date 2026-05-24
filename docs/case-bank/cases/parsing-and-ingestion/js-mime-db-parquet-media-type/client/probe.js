const db = require("mime-db");
const entry = db["application/vnd.apache.parquet"] || null;
console.log(JSON.stringify({ exists: !!entry, extensions: entry && entry.extensions ? entry.extensions : null }));
