#!/usr/bin/env python3
"""Generate WhatsApp system status HTML page"""
import json, os, subprocess, sqlite3
from datetime import datetime

DB = "C:/nichenexusglobal/whatsapp_mail.db"
JSONL = "C:/nichenexusglobal/whatsapp_messages.jsonl"
HTML = "C:/nichenexusglobal/status.html"

# Collect status data
status = {}

# Bridge health
try:
    r = subprocess.run(["curl","-s","--max-time","3","http://127.0.0.1:3000/health"],
        capture_output=True, text=True, timeout=5)
    bdata = json.loads(r.stdout) if r.stdout else {}
    status["bridge"] = {"ok": "connected" in r.stdout, "data": bdata}
except:
    status["bridge"] = {"ok": False, "data": {"error": "unreachable"}}

# wago-api health
try:
    r = subprocess.run(["curl","-s","--max-time","3","http://127.0.0.1:3003/health"],
        capture_output=True, text=True, timeout=5)
    wdata = json.loads(r.stdout) if r.stdout else {}
    connected = wdata.get("sessions", [{}])[0].get("connected", False) if wdata.get("sessions") else False
    status["wago"] = {"ok": connected, "data": wdata}
except:
    status["wago"] = {"ok": False, "data": {"error": "unreachable"}}

# Database stats
try:
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    total = c.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    sent = c.execute("SELECT COUNT(*) FROM messages WHERE is_from_me=1").fetchone()[0]
    recv = c.execute("SELECT COUNT(*) FROM messages WHERE is_from_me=0").fetchone()[0]
    unread = c.execute("SELECT COUNT(*) FROM messages WHERE is_from_me=0 AND is_read=0 AND chat_id NOT LIKE '%81609428590707%'").fetchone()[0]
    last_recv = c.execute("SELECT body, sender_name, timestamp FROM messages WHERE is_from_me=0 AND chat_id NOT LIKE '%81609428590707%' ORDER BY timestamp DESC LIMIT 1").fetchone()
    conn.close()
    status["db"] = {"ok": True, "total": total, "sent": sent, "recv": recv, "unread": unread, "last_recv_body": str(last_recv[0] or "")[:80] if last_recv else "", "last_recv_from": str(last_recv[1] or "")[:30] if last_recv else "", "last_recv_ts": last_recv[2] if last_recv else 0}
except:
    status["db"] = {"ok": False}

# JSONL size
try:
    jsonl_size = os.path.getsize(JSONL)
    status["jsonl"] = {"ok": True, "size_kb": jsonl_size // 1024}
except:
    status["jsonl"] = {"ok": False}

# Startup launcher
status["startup"] = os.path.exists(os.path.expanduser("~") + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/Start_WhatsApp_Bridge.bat")

# Generate HTML
html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta http-equiv="refresh" content="10">
<title>NNG WhatsApp Status</title>
<style>
body{{font-family:'Segoe UI',sans-serif;background:#0d1117;color:#c9d1d9;margin:20px}}
.card{{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;margin:12px 0}}
.status{{display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:8px}}
.green{{background:#3fb950}}
.red{{background:#f85149}}
.yellow{{background:#d29922}}
h1{{color:#58a6ff}}h2{{color:#8b949e;font-size:14px;text-transform:uppercase;letter-spacing:1px}}
table{{width:100%;border-collapse:collapse}}
td{{padding:6px 8px;border-bottom:1px solid #21262d}}
.key{{color:#8b949e;width:160px}}
.val{{color:#c9d1d9}}
.timestamp{{color:#484f58;font-size:12px;text-align:right}}
</style></head>
<body>
<h1>🔍 NNG WhatsApp Status</h1>
<div class="timestamp">Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>

<div class="card">
<h2>Infrastructure</h2>
<table>
<tr><td class="key"><span class="status {'green' if status['wago']['ok'] else 'red'}"></span>wago-api</td>
<td class="val">{'CONNECTED' if status['wago']['ok'] else 'DISCONNECTED'}</td></tr>
<tr><td class="key"><span class="status {'green' if status['bridge']['ok'] else 'red'}"></span>Bridge</td>
<td class="val">{'Connected' if status['bridge']['ok'] else 'Disconnected'} (uptime: {status['bridge']['data'].get('uptime',0):.0f}s)</td></tr>
<tr><td class="key"><span class="status {'green' if status['startup'] else 'red'}"></span>Auto-start</td>
<td class="val">{'Installed' if status['startup'] else 'Missing'}</td></tr>
</table>
</div>

<div class="card">
<h2>Mailbox</h2>
<table>
<tr><td class="key"><span class="status {'green' if status['db'].get('ok') else 'red'}"></span>Database</td><td class="val">{status['db'].get('total',0)} messages ({status['db'].get('sent',0)} sent, {status['db'].get('recv',0)} received)</td></tr>
<tr><td class="key">📥 Unread</td><td class="val">{status['db'].get('unread',0)}</td></tr>
<tr><td class="key">📤 JSONL</td><td class="val">{status['jsonl'].get('size_kb',0)} KB</td></tr>
<tr><td class="key">Last received</td><td class="val">{status['db'].get('last_recv_from','-')}: {status['db'].get('last_recv_body','-')}</td></tr>
</table>
</div>

<div class="card">
<h2>System</h2>
<table>
<tr><td class="key">💾 Backup</td><td class="val">Daily 21:00 (GitHub + local)</td></tr>
<tr><td class="key">🔔 Watchdog</td><td class="val">Every 1 min (auto-restart bridge)</td></tr>
<tr><td class="key">🔄 Auto-start</td><td class="val">On login (Startup folder)</td></tr>
</table>
</div>

<p style="color:#484f58;text-align:center;font-size:12px;margin-top:30px">
All green = system healthy. Any red = needs attention.<br>
Page auto-refreshes every 10 seconds.
</p>
</body></html>"""

with open(HTML, "w") as f:
    f.write(html)

# Determine overall status
all_ok = status['wago']['ok'] and status['bridge']['ok'] and status['db'].get('ok')
overall = "✅ ALL GREEN" if all_ok else "❌ ISSUES"
print(f"Status: {overall}")
print(f"  wago-api: {'CONNECTED' if status['wago']['ok'] else 'DOWN'}")
print(f"  bridge:   {'UP' if status['bridge']['ok'] else 'DOWN'}")
print(f"  DB:       {status['db'].get('total',0)} msgs, {status['db'].get('unread',0)} unread")
print(f"  HTML:     file:///C:/nichenexusglobal/status.html")
