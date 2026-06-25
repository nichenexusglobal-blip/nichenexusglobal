"""Search for M Million messages - check both formats"""
import json

with open("C:/nichenexusglobal/whatsapp_messages.jsonl", "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

# Search for Million or 2349
print("=== 搜索 Million / 2349 ===")
for line in reversed(lines):
    line = line.strip()
    if not line:
        continue
    lower = line.lower()
    if "million" not in lower and "2349" not in line:
        continue
    
    try:
        d = json.loads(line)
    except:
        continue
    
    data = d.get("data", {})
    is_me = data.get("isFromMe", False)
    chat = data.get("chat", "")
    body = data.get("body", "") or ""
    
    # Also check body
    msg_data = data.get("message", {})
    conv = msg_data.get("conversation", "") or msg_data.get("extendedTextMessage", {}).get("text", "") or ""
    
    text = body or conv
    if not text:
        continue
    
    push = data.get("pushName", "?")
    
    tag = "→ SENT" if is_me else "→ RECV"
    print(f"\n{tag} | push:{push} | chat:{chat}")
    print(f"  {text[:200]}")
