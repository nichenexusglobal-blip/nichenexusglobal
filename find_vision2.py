"""Find all Vision Africa / TO-GO mentions in JSONL - check both chat IDs"""
import json

with open("C:/nichenexusglobal/whatsapp_messages.jsonl", "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

chats_seen = set()
for line in reversed(lines):
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
    except:
        continue
    
    data = d.get("data", {})
    chat = data.get("chat", "")
    push_name = data.get("pushName", "") or ""
    msg = data.get("message", {})
    conv = msg.get("conversation", "") or msg.get("extendedTextMessage", {}).get("text", "") or ""
    
    # Check Vision Africa keywords
    keywords = ["vision", "TO-GO", "to-go", "T O G O", "africa"]
    matched = any(k in str(chat).lower() or k in str(conv).lower() or k in str(push_name).lower() for k in keywords)
    
    if matched:
        is_me = data.get("isFromMe", False)
        from_me = "→ OUR MSG" if is_me else "→ THEIR MSG"
        ts = d.get("timestamp", "")
        print(f"{from_me} | {ts} | chat={chat} | pushName={push_name}")
        print(f"  {conv[:300]}")
        print()

# Also search for 2348168510007 specifically
print("\n=== Search by phone 2348168510007 ===")
for line in reversed(lines):
    line = line.strip()
    if not line or "2348168510007" not in line:
        continue
    try:
        d = json.loads(line)
    except:
        continue
    data = d.get("data", {})
    is_me = data.get("isFromMe", False)
    msg = data.get("message", {})
    conv = msg.get("conversation", "") or msg.get("extendedTextMessage", {}).get("text", "") or ""
    ts = d.get("timestamp", "")
    print(f"{'→ OUR MSG' if is_me else '→ THEIR MSG'} | {ts}")
    print(f"  {conv[:400]}")
    print()
