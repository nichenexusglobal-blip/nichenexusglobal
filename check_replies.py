"""Check real WhatsApp replies - only new, non-auto"""
import json

with open("C:/nichenexusglobal/whatsapp_messages.jsonl") as f:
    lines = f.readlines()

real = []
for line in lines:
    line = line.strip()
    if not line: continue
    try:
        d = json.loads(line)
    except:
        continue
    if d.get("data",{}).get("isFromMe",True): continue
    pn = d.get("data",{}).get("pushName","")
    msg = d.get("data",{}).get("message",{}).get("conversation","")
    if not msg: continue
    # Skip obvious auto-replies
    if any(k in msg.lower() for k in ["welcome","thank you for","auto","terima kasih"]): continue
    real.append(f"{pn}: {msg[:100]}")

print(f"Non-auto replies: {len(real)}")
for r in real[-5:]:
    print(f"  {r}")
