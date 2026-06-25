"""Check WhatsApp for Pecron/Chris OEM picture"""
import json

with open("C:/nichenexusglobal/whatsapp_messages.jsonl", "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

# Search for Pecron / Chris / 1536147
print("=== WhatsApp: Pecron / Chris ===")
for line in reversed(lines):
    line = line.strip()
    if not line:
        continue
    lower = line.lower()
    if "pecron" not in lower and "chris" not in lower and "1536147" not in line and "sales06" not in lower:
        continue
    
    try:
        d = json.loads(line)
    except:
        continue
    
    data = d.get("data", {})
    is_me = data.get("isFromMe", False)
    chat = data.get("chat", "")
    body = data.get("body", "") or ""
    msg_data = data.get("message", {})
    conv = msg_data.get("conversation", "") or ""
    text = body or conv
    
    tag = "→ SENT" if is_me else "→ RECV"
    ts = d.get("timestamp", "") or d.get("_received_at", "")
    
    print(f"\n{tag} | {str(ts)[:19]} | chat={chat}")
    print(f"  {text[:200]}")
