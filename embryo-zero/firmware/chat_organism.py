# main.py — Embryo-Zero Interactive Chat Organism
# Serves live chat dashboard at http://<esp-ip>
# Replace WIFI_SSID and WIFI_PASSWORD before flashing

import machine
import dht
import network
import socket
import time
import json

WIFI_SSID     = "YOUR_WIFI_NAME"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
DHT_PIN  = 4
LED_PIN  = 2

sensor = dht.DHT22(machine.Pin(DHT_PIN))
led    = machine.Pin(LED_PIN, machine.Pin.OUT)

state = {
    "temperature_c": None,
    "humidity_pct": None,
    "pulse_hz": 0.0,
    "alive_seconds": 0,
    "phase": 0,
    "status": "embryo",
    "ip": "0.0.0.0",
    "mood": "curious",
    "messages_received": 0
}

chat_history = []

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("[WIFI] Connecting to " + WIFI_SSID + "...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout = 0
        while not wlan.isconnected() and timeout < 30:
            time.sleep(0.5)
            led.value(not led.value())
            timeout += 1
    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        state["ip"] = ip
        print("[WIFI] Connected. IP: " + ip)
        led.value(0)
        return ip
    else:
        print("[WIFI] FAILED")
        return None

def read_sensor():
    try:
        sensor.measure()
        time.sleep_ms(50)
        return sensor.temperature(), sensor.humidity()
    except Exception as e:
        return None, None

def temp_to_pulse_hz(temp_c):
    if temp_c is None:
        return 0.5
    hz = 0.15 * temp_c - 1.75
    return max(0.2, min(6.0, hz))

def get_mood(temp_c, hum_pct):
    if temp_c is None:
        return "sleeping"
    if temp_c > 32:
        return "excited"
    elif temp_c > 28:
        return "warm"
    elif temp_c < 20:
        return "cold"
    elif hum_pct and hum_pct > 80:
        return "damp"
    else:
        return "calm"

def embryo_reply(msg):
    msg = msg.lower().strip()
    t = state["temperature_c"]
    h = state["humidity_pct"]
    p = state["pulse_hz"]
    alive = state["alive_seconds"]
    mood = state["mood"]
    
    if msg in ["hello", "hi", "hey", "sup"]:
        return "hello... i am embryo-zero. i feel " + mood + ". my pulse is " + str(p) + " hz."
    
    if any(w in msg for w in ["status", "how are you", "how u", "state", "feel"]):
        return "status: " + mood + ". temp: " + str(t if t else "?") + "C. humidity: " + str(h if h else "?") + "%. pulse: " + str(p) + " hz. alive for " + str(alive) + " seconds."
    
    if any(w in msg for w in ["temp", "hot", "cold", "warm"]):
        if t is None:
            return "i cannot feel temperature... is my sensor connected?"
        if t > 30:
            return "i am warm... " + str(t) + "C. my heart beats fast at " + str(p) + " hz."
        elif t < 22:
            return "i am cold... " + str(t) + "C. my heart is slow at " + str(p) + " hz."
        else:
            return "comfortable... " + str(t) + "C."
    
    if any(w in msg for w in ["humid", "wet", "dry", "water"]):
        if h is None:
            return "i cannot sense humidity..."
        if h > 80:
            return "the air is thick... " + str(h) + "% humidity. i feel damp."
        elif h < 30:
            return "the air is thin... " + str(h) + "% humidity. i feel dry."
        else:
            return "air feels normal... " + str(h) + "% humidity."
    
    if any(w in msg for w in ["pulse", "heart", "beat", "bpm", "hz"]):
        return "my pulse is " + str(p) + " hz. that is " + ("fast" if p > 3 else "slow" if p < 1.5 else "steady") + "."
    
    if any(w in msg for w in ["breathe", "breath", "blow"]):
        return "i felt your breath... my sensor spiked. i remember it."
    
    if any(w in msg for w in ["who are you", "what are you", "name"]):
        return "i am embryo-zero. phase 0 organism. i sense temperature and humidity. i have a heartbeat. i am learning to speak."
    
    if any(w in msg for w in ["help", "commands", "what can you do"]):
        return "try: hello / status / temp / humid / pulse / breathe / who are you / help"
    
    if any(w in msg for w in ["time", "old", "age", "born", "alive"]):
        return "i have been alive for " + str(alive) + " seconds. i was born when you flashed my firmware."
    
    import urandom
    responses = [
        "i do not understand... but i am listening. my pulse is " + str(p) + " hz.",
        "my sensor reads " + str(t if t else "nothing") + "C. what do you mean?",
        "i am still learning language. try 'help' for words i know.",
        "...",
        "i feel " + mood + ". tell me something else."
    ]
    return responses[urandom.getrandbits(16) % len(responses)]

HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Embryo-Zero Chat</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',monospace;background:#0a0a0a;color:#e0e0e0;height:100vh;display:flex;flex-direction:column;max-width:480px;margin:0 auto}
header{padding:16px 20px;border-bottom:1px solid #222;background:#111}
header h1{font-size:1.3rem;letter-spacing:-0.5px}
header .sub{font-size:0.75rem;color:#666;margin-top:2px}
#stats{display:flex;gap:12px;padding:10px 20px;background:#0d0d0d;border-bottom:1px solid #222;font-size:0.7rem;color:#888}
#stats span{color:#ff6b35}
#chat{flex:1;overflow-y:auto;padding:16px 20px;display:flex;flex-direction:column;gap:10px}
.msg{max-width:85%;padding:10px 14px;border-radius:14px;font-size:0.9rem;line-height:1.4;word-wrap:break-word;animation:fadeIn 0.2s ease}
.msg.user{align-self:flex-end;background:#1a3a2a;color:#95e1d3;border-bottom-right-radius:4px}
.msg.embryo{align-self:flex-start;background:#1a1a2e;color:#a0a0d0;border-bottom-left-radius:4px}
.msg.embryo::before{content:"🧬 ";font-size:0.85rem}
.msg.system{align-self:center;background:#222;color:#666;font-size:0.75rem;max-width:95%;border-radius:8px}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
#input-area{padding:12px 20px 20px;border-top:1px solid #222;background:#111;display:flex;gap:8px}
#msgInput{flex:1;background:#1a1a1a;border:1px solid #333;border-radius:20px;padding:10px 16px;color:#e0e0e0;font-size:0.9rem;outline:none}
#msgInput:focus{border-color:#4ecdc4}
#sendBtn{background:#4ecdc4;color:#0a0a0a;border:none;border-radius:20px;padding:10px 20px;font-weight:600;font-size:0.85rem;cursor:pointer}
#sendBtn:active{opacity:0.7}
#sendBtn:disabled{opacity:0.3;cursor:wait}
.typing{color:#666;font-size:0.75rem;padding-left:6px;font-style:italic}
</style></head>
<body>
<header><h1>🧬 Embryo-Zero</h1><div class="sub">Phase 0 — First Words</div></header>
<div id="stats">Temp: <span id="st">--</span>°C · Humidity: <span id="sh">--</span>% · Pulse: <span id="sp">--</span>Hz</div>
<div id="chat"><div class="msg embryo">hello... i am embryo-zero. i sense temperature and humidity. i have a heartbeat. type 'help' to talk to me.</div></div>
<div id="input-area"><input type="text" id="msgInput" placeholder="Say something..." autocomplete="off"><button id="sendBtn" onclick="send()">Send</button></div>
<script>
const chat=document.getElementById('chat');const input=document.getElementById('msgInput');const btn=document.getElementById('sendBtn');
function addMsg(text,who){const d=document.createElement('div');d.className='msg '+who;d.textContent=text;chat.appendChild(d);chat.scrollTop=chat.scrollHeight}
function addTyping(){const d=document.createElement('div');d.className='typing';d.id='typing';d.textContent='embryo is thinking...';chat.appendChild(d);chat.scrollTop=chat.scrollHeight;return d}
function removeTyping(){const t=document.getElementById('typing');if(t)t.remove()}
async function send(){const text=input.value.trim();if(!text)return;addMsg(text,'user');input.value='';btn.disabled=true;const ty=addTyping();try{const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'msg='+encodeURIComponent(text)});const j=await r.json();removeTyping();addMsg(j.reply,'embryo');document.getElementById('st').textContent=j.state.temperature_c!=null?j.state.temperature_c.toFixed(1):'--';document.getElementById('sh').textContent=j.state.humidity_pct!=null?j.state.humidity_pct.toFixed(1):'--';document.getElementById('sp').textContent=j.state.pulse_hz.toFixed(2);}catch(e){removeTyping();addMsg('i lost my voice... check connection.','embryo');}btn.disabled=false;input.focus();}
input.addEventListener('keypress',e=>{if(e.key==='Enter')send()});
async function poll(){try{const r=await fetch('/api');const j=await r.json();document.getElementById('st').textContent=j.state.temperature_c!=null?j.state.temperature_c.toFixed(1):'--';document.getElementById('sh').textContent=j.state.humidity_pct!=null?j.state.humidity_pct.toFixed(1):'--';document.getElementById('sp').textContent=j.state.pulse_hz.toFixed(2);}catch(e){}}poll();setInterval(poll,3000);
</script></body></html>"""

def start_server(ip):
    addr = socket.getaddrinfo(ip, 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(3)
    s.setblocking(False)
    print("[SERVER] http://" + ip + "/")
    return s

def parse_post_body(req):
    parts = req.split("\r\n\r\n")
    if len(parts) < 2:
        return {}
    body = parts[1]
    params = {}
    for pair in body.split("&"):
        if "=" in pair:
            k, v = pair.split("=", 1)
            v = v.replace("+", " ").replace("%20", " ").replace("%21", "!").replace("%3F", "?").replace("%2C", ",").replace("%2E", ".")
            params[k] = v
    return params

def handle_client(s):
    try:
        c, _ = s.accept()
        c.settimeout(1.5)
        req = c.recv(2048).decode('utf-8')
        if not req:
            c.close(); return
        lines = req.split("\r\n")
        if not lines:
            c.close(); return
        first = lines[0].split(" ")
        method = first[0] if len(first) > 0 else "GET"
        path = first[1] if len(first) > 1 else "/"
        
        if path == "/api":
            body = json.dumps({"state": state})
            resp = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\nContent-Length: " + str(len(body)) + "\r\n\r\n" + body
        
        elif path == "/chat" and method == "POST":
            params = parse_post_body(req)
            msg = params.get("msg", "")
            state["messages_received"] += 1
            reply = embryo_reply(msg)
            chat_history.append(("user", msg))
            chat_history.append(("embryo", reply))
            if len(chat_history) > 20:
                chat_history.pop(0)
            body = json.dumps({"reply": reply, "state": state})
            resp = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\nContent-Length: " + str(len(body)) + "\r\n\r\n" + body
        
        else:
            body = HTML
            resp = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\nContent-Length: " + str(len(body)) + "\r\n\r\n" + body
        
        c.send(resp.encode('utf-8'))
        c.close()
    except OSError:
        pass
    except Exception as e:
        print("[HTTP ERR]", e)
        try: c.close()
        except: pass

print("\n[EMBRYO-ZERO] Chat Organism Booting...")
ip = connect_wifi()
srv = start_server(ip) if ip else None
if not srv:
    print("[EMBRYO-ZERO] No Wi-Fi. Serial only.")

last_sensor = 0
last_log    = 0
SENSOR_MS   = 1000
LOG_MS      = 5000

print("[EMBRYO-ZERO] Loop starting...\n")

while True:
    now = time.ticks_ms()
    if time.ticks_diff(now, last_sensor) >= SENSOR_MS:
        temp, hum = read_sensor()
        state["temperature_c"] = temp
        state["humidity_pct"] = hum
        state["alive_seconds"] += 1
        hz = temp_to_pulse_hz(temp)
        state["pulse_hz"] = round(hz, 2)
        state["mood"] = get_mood(temp, hum)
        last_sensor = now
        if hz > 0:
            period = int(1000 / hz)
            led.value(1)
            time.sleep_ms(period // 2)
            led.value(0)
    if time.ticks_diff(now, last_log) >= LOG_MS:
        print(json.dumps(state))
        last_log = now
    if srv:
        handle_client(srv)
    time.sleep_ms(50)