import builtinModules from "builtin-modules";
console.log(JSON.stringify({ hasNodeFfi: builtinModules.includes("node:ffi"), count: builtinModules.length }));
