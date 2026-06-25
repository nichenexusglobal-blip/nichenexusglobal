"""Quick channel scan — new messages since last check"""
import json

# Check JSONL for new incoming messages
with open("C:/nichenexusglobal/whatsapp_messages.jsonl", "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

# Find the last incoming messages we haven't processed
seen = set()
recent_incoming = []
for line in reversed(lines):
    if len(recent_incoming) >= 5:
        break
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
    except:
        continue
    
    data = d.get("data", {})
    is_me = data.get("isFromMe", True)
    if is_me:
        continue
    
    msg = data.get("body", "") or ""
    if not msg:
        # Try to find message in nested structures
        msg_data = data.get("message", {})
        msg = msg_data.get("conversation", "") or ""
    
    if not msg:
        continue
    
    push = data.get("pushName", "?")
    chat = data.get("chat", "?")
    ts = d.get("timestamp", "") or d.get("_received_at", "")
    
    key = f"{chat}|{msg[:30]}"
    if key in seen:
        continue
    seen.add(key)
    
    recent_incoming.append({
        "from": push,
        "chat": chat,
        "msg": msg[:200],
        "time": str(ts)[:19]
    })

print("=== 最近入消息 ===")
if recent_incoming:
    for r in recent_incoming:
        print(f"\n💬 {r['from']}")
        print(f"   {r['msg']}")
        print(f"   ⏰ {r['time']}")
else:
    print("无新入消息")

# Also check pending items
print("\n\n=== 待处理 ===")
print("🔴 Vision Africa — 已回 ✅（刚才）")
print("🟡 Taico (Kelly) — 上周发了跟进，等回复")
print("🟡 SOUOP/Pordie — 上周发了询盘，等回复")
print("🟡 M Million — 有未回消息")
print("🟡 KWT Tech Mart — 已发邮件报价，等回复")
