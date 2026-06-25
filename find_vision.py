"""Find Vision Africa messages in JSONL"""
import json

with open("C:/nichenexusglobal/whatsapp_messages.jsonl", "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

for line in reversed(lines):
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
    except:
        continue
    
    # Check chat_id for Vision Africa
    data = d.get("data", {})
    chat = data.get("chat", "")
    
    if "2348168510007" in chat or "vision" in chat.lower():
        is_me = data.get("isFromMe", False)
        msg = data.get("message", {})
        conv = msg.get("conversation", "") or msg.get("extendedTextMessage", {}).get("text", "")
        from_me = "→ SENT" if is_me else "→ RECV"
        print(f"{from_me} | {d.get('event','')} | chat={chat}")
        print(f"  {conv[:300]}")
        print()
