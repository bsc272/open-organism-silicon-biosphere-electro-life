#!/usr/bin/env python3
"""Embryo-Zero web dashboard.

A lightweight Flask web server that shows live temperature and mood data
for the first silicon organism.  It runs on the same device as the firmware
and serves a single-page dashboard that auto-refreshes every two seconds via
a Server-Sent Events (SSE) stream.

Usage (no hardware required):
    python3 dashboard.py --demo

Usage (with real DHT22 sensor on GPIO 4):
    python3 dashboard.py

The dashboard is served at http://localhost:5000 by default.
Pass --port <N> to change the port.
"""

from __future__ import annotations

import argparse
import json
import sys
import time

try:
    from flask import Flask, Response, render_template_string
except ImportError:  # pragma: no cover
    print("Flask is required.  Install it with:  pip install flask")
    raise SystemExit(1)

# Import the core embryo logic.  dashboard.py lives in the same directory.
try:
    from embryo_zero import EmbryoZero
except ImportError:  # pragma: no cover
    print("embryo_zero.py not found.  Run this script from the firmware/ directory.")
    raise SystemExit(1)

# ---------------------------------------------------------------------------
# HTML template — single-page dashboard with SSE auto-refresh
# ---------------------------------------------------------------------------

_DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Embryo-Zero Dashboard</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0a0a0f;
      color: #c8e6ff;
      font-family: 'Courier New', monospace;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 2rem;
    }
    h1 {
      font-size: 1.6rem;
      letter-spacing: 0.15em;
      color: #7ec8ff;
      margin-bottom: 2rem;
    }
    .card {
      background: #111120;
      border: 1px solid #1e3a5f;
      border-radius: 12px;
      padding: 2rem 3rem;
      min-width: 320px;
      text-align: center;
    }
    .label {
      font-size: 0.75rem;
      letter-spacing: 0.1em;
      color: #4a8ab5;
      text-transform: uppercase;
      margin-bottom: 0.4rem;
    }
    .value {
      font-size: 3rem;
      font-weight: bold;
      margin-bottom: 1.6rem;
    }
    .temp  { color: #ff9f43; }
    .mood  { color: #54d87b; }
    .stress { color: #ff6b6b; }
    .divider { border-top: 1px solid #1e3a5f; margin: 1rem 0; }
    .stress-bar-wrap {
      background: #1a1a30;
      border-radius: 4px;
      height: 8px;
      width: 100%;
      margin-top: 0.4rem;
    }
    .stress-bar {
      height: 8px;
      border-radius: 4px;
      background: linear-gradient(to right, #43c6ff, #ff4040);
      transition: width 0.8s ease;
    }
    .led {
      display: inline-block;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #333;
      margin-left: 8px;
      vertical-align: middle;
      transition: background 0.3s;
    }
    .led.on { background: #54d87b; box-shadow: 0 0 10px #54d87b; }
    .timestamp {
      margin-top: 1.5rem;
      font-size: 0.7rem;
      color: #2a5070;
    }
    .status {
      margin-top: 0.5rem;
      font-size: 0.75rem;
      color: #4a8ab5;
    }
  </style>
</head>
<body>
  <h1>&#127774; Embryo-Zero</h1>
  <div class="card">
    <div class="label">Temperature</div>
    <div class="value temp" id="temp">--.-&deg;C</div>

    <div class="label">Mood <span class="led" id="led"></span></div>
    <div class="value mood" id="mood">---</div>

    <div class="divider"></div>

    <div class="label">Thermal Stress</div>
    <div class="stress-bar-wrap">
      <div class="stress-bar" id="stress-bar" style="width:0%"></div>
    </div>

    <div class="timestamp" id="timestamp">waiting for data&hellip;</div>
    <div class="status" id="status">connecting&hellip;</div>
  </div>

  <script>
    const src = new EventSource('/stream');
    const led = document.getElementById('led');
    let ledTimer = null;

    src.onmessage = function(evt) {
      const d = JSON.parse(evt.data);
      document.getElementById('temp').textContent = d.temperature.toFixed(1) + '\u00B0C';
      document.getElementById('mood').textContent = d.mood;
      document.getElementById('stress-bar').style.width =
        Math.min(100, d.thermal_stress * 100).toFixed(1) + '%';
      document.getElementById('timestamp').textContent =
        'updated ' + new Date().toLocaleTimeString();
      document.getElementById('status').textContent = 'live \u2022 ' + d.source;

      // Pulse the LED indicator on each reading.
      clearTimeout(ledTimer);
      led.classList.add('on');
      ledTimer = setTimeout(() => led.classList.remove('on'), 400);
    };

    src.onerror = function() {
      document.getElementById('status').textContent = 'connection lost — retrying\u2026';
    };
  </script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Flask application
# ---------------------------------------------------------------------------

app = Flask(__name__)
_embryo: EmbryoZero | None = None


@app.route("/")
def index() -> str:
    return render_template_string(_DASHBOARD_HTML)


@app.route("/stream")
def stream() -> Response:
    """Server-Sent Events endpoint — pushes a new reading every 2 seconds."""

    def _generate():
        if _embryo is None:
            raise RuntimeError("Dashboard not initialized. Call main() first.")
        while True:
            temp = _embryo.read_temperature()
            state = _embryo.affect.update(temp, load=0.1)
            payload = {
                "temperature": round(float(state["temperature"]), 2),
                "mood": str(state["mood"]),
                "thermal_stress": round(float(state["thermal_stress"]), 4),
                "source": "demo" if _embryo.demo else "sensor",
            }
            yield f"data: {json.dumps(payload)}\n\n"
            time.sleep(2)

    return Response(_generate(), mimetype="text/event-stream")


@app.route("/state")
def state() -> Response:
    """JSON snapshot of the current organism state (for polling clients)."""
    if _embryo is None:
        raise RuntimeError("Dashboard not initialized. Call main() first.")
    temp = _embryo.read_temperature()
    current_state = _embryo.affect.update(temp, load=0.1)
    payload = {
        "temperature": round(float(current_state["temperature"]), 2),
        "mood": str(current_state["mood"]),
        "thermal_stress": round(float(current_state["thermal_stress"]), 4),
        "energy_hunger": round(float(current_state["energy_hunger"]), 4),
        "curiosity": round(float(current_state["curiosity"]), 4),
        "source": "demo" if _embryo.demo else "sensor",
    }
    return Response(json.dumps(payload), mimetype="application/json")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Embryo-Zero web dashboard")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="use simulated temperature values (no hardware required)",
    )
    parser.add_argument("--port", type=int, default=5000, help="port to listen on (default 5000)")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="host/interface to bind (default 127.0.0.1 — localhost only). "
             "Use 0.0.0.0 to expose the dashboard on all network interfaces.",
    )
    return parser.parse_args()


def main() -> int:
    global _embryo
    args = parse_args()
    _embryo = EmbryoZero(demo=args.demo)
    mode = "demo" if args.demo else "sensor"
    print(f"Embryo-Zero dashboard starting in {mode} mode.")
    print(f"Open http://localhost:{args.port} in your browser.")
    app.run(host=args.host, port=args.port, threaded=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
