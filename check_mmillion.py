"""Check M Million messages and reply"""
import json

with open("C:/nichenexusglobal/whatsapp_messages.jsonl", "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

# Find M Million / 2349164337200 messages
print("=== M Million 对话 ===")
for line in reversed(lines):
    line = line.strip()
    if not line or "2349164337200" not in line:
        continue
    try:
        d = json.loads(line)
    except:
        continue
    
    data = d.get("data", {})
    is_me = data.get("isFromMe", False)
    body = data.get("body", "") or ""
    ts = d.get("timestamp", "") or d.get("_received_at", "")
    
    tag = "→ OUR MSG" if is_me else "→ THEIR MSG"
    print(f"\n{tag} | {str(ts)[:19]}")
    print(f"  {body[:300]}")
