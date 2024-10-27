const express = require("express");
const path = require("path");
const { createProxyMiddleware } = require("http-proxy-middleware");

const app = express();

app.use(express.static(path.join(__dirname, "build")));

app.use(
  "/api",
  createProxyMiddleware({
    target: "http://krakend:8080",
    changeOrigin: true,
  }),
);

app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "build", "index.html"));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Express server running on port ${PORT}`);
});
