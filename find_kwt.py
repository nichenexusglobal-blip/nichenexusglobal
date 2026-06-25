"""Find KWT Tech Mart chat ID and send quote via WhatsApp"""
import json

with open("C:/nichenexusglobal/whatsapp_messages.jsonl", "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

# Find KWT Tech Mart
for line in reversed(lines):
    line = line.strip()
    if not line:
        continue
    if "kwt" not in line.lower() and "KWT" not in line and "kwttechmart" not in line.lower():
        continue
    
    try:
        d = json.loads(line)
    except:
        continue
    
    data = d.get("data", {})
    chat = data.get("chat", "")
    body = data.get("body", "") or ""
    is_me = data.get("isFromMe", False)
    
    print(f"{'→ SENT' if is_me else '→ RECV'} | chat={chat}")
    print(f"  {body[:200]}")
    print()
