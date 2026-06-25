"""Check WhatsApp replies"""
import json
with open("C:/nichenexusglobal/whatsapp_messages.jsonl") as f:
    lines = f.readlines()

new = []
for line in lines:
    line=line.strip()
    if not line: continue
    try:
        d = json.loads(line)
    except:
        continue
    if not d.get("data", {}).get("isFromMe", True):
        t = d.get("data", {}).get("pushName", d.get("data", {}).get("jid", "?"))
        msg = d.get("data", {}).get("message", {}).get("conversation", "")
        if msg:
            new.append({"from": t, "msg": msg[:80]})

print(f"Total new incoming: {len(new)}")
for n in new[-5:]:
    print(f"  {n['from']}: {n['msg']}")
