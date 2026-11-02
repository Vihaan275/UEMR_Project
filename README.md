# SOS demo

Barebones emergency demo: a caller hits **SOS**, dispatch sees their GPS pin and can open directions.

## Run it

You need **Python 3**. No packages to install.

```bash
python server.py
```

On some machines that's `python3` instead of `python`.

Then open two tabs:

| Role | URL |
| --- | --- |
| Caller (SOS button) | http://localhost:3000/ |
| Dispatch / EMTs | http://localhost:3000/dispatch.html |

## Demo flow

1. Leave the dispatch tab open.
2. On the caller tab, click **SOS** and allow location.
3. Dispatch should pick up the alert within a couple of seconds, show a map pin, and offer **Get directions** (Google Maps from the responder's location).

Alerts are stored in memory only. Restarting the server clears them.

## Two phones / laptops on the same Wi‑Fi

The server prints `http://localhost:3000/`. On another device, swap `localhost` for the host computer's local IP, for example `http://192.168.x.x:3000/`.

Browsers usually only share GPS on `localhost` or HTTPS. If location is blocked on a phone over `http://`, run the caller page on the same machine as the server, or use a tunnel such as [ngrok](https://ngrok.com/) if you need a real phone demo.

Stop the server with `Ctrl+C`.
