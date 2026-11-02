import json
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent / "public"
alerts = []
MAX = 30


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        if urlparse(self.path).path == "/api/alerts":
            return self.json(200, alerts)
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/sos":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
            lat, lng = float(body["lat"]), float(body["lng"])
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            return self.json(400, {"error": "Need lat and lng"})

        alert = {
            "id": format(int(time.time() * 1000), "x"),
            "lat": lat,
            "lng": lng,
            "accuracy": body.get("accuracy"),
            "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        alerts.insert(0, alert)
        del alerts[MAX:]
        self.json(200, alert)

    def json(self, code, data):
        raw = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    port = 3000
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print("SOS user page:    http://localhost:%s/" % port)
    print("Dispatch / EMTs:  http://localhost:%s/dispatch.html" % port)
    server.serve_forever()
