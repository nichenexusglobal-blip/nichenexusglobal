"""Check last incoming messages in JSONL"""
import json

with open("C:/nichenexusglobal/whatsapp_messages.jsonl") as f:
    lines = f.readlines()

seen = set()
for line in reversed(lines):
    line = line.strip()
    if not line: continue
    try:
        d = json.loads(line)
    except:
        continue
    if d.get("data",{}).get("isFromMe",True): continue
    pn = d.get("data",{}).get("pushName","?")
    msg = d.get("data",{}).get("message",{}).get("conversation","")
    if not msg: continue
    key = f"{pn}: {msg[:50]}"
    if key in seen: continue
    seen.add(key)
    print(key)
