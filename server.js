const express = require("express");
const os = require("os");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

const alerts = [];
const MAX = 30;

app.get("/api/alerts", (_req, res) => {
  res.json(alerts);
});

app.post("/api/sos", (req, res) => {
  const { lat, lng, accuracy } = req.body || {};
  if (typeof lat !== "number" || typeof lng !== "number") {
    return res.status(400).json({ error: "Need lat and lng" });
  }

  const alert = {
    id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
    lat,
    lng,
    accuracy: typeof accuracy === "number" ? accuracy : null,
    time: new Date().toISOString(),
  };

  alerts.unshift(alert);
  if (alerts.length > MAX) alerts.pop();

  res.json(alert);
});

app.listen(PORT, "0.0.0.0", () => {
  const nets = os.networkInterfaces();
  const urls = [`http://localhost:${PORT}`];
  for (const list of Object.values(nets)) {
    for (const net of list || []) {
      if (net.family === "IPv4" && !net.internal) {
        urls.push(`http://${net.address}:${PORT}`);
      }
    }
  }
  console.log("SOS user page:      " + urls[0] + "/");
  console.log("Dispatch / EMTs:    " + urls[0] + "/dispatch.html");
  if (urls.length > 1) {
    console.log("On this network:    " + urls[1] + "/");
  }
});
