const esbuild = require("esbuild")

esbuild
  .build({
    entryPoints: ["src/scripts/app.js"],
    bundle: true,
    outfile: "static/scripts/app.js",
  })
  .catch(() => process.exit(1))
