#!/usr/bin/env python3
"""Extract full Vision Africa conversation + research"""
import json

# 1. WhatsApp conversation
print("=== WHATSAPP CONVERSATION ===")
with open("C:/nichenexusglobal/whatsapp_messages.jsonl") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        if "Vision" not in line and "196795552559" not in line and "TO-GO" not in line and "togo" not in line.lower():
            continue
        try:
            msg = json.loads(line)
            data = msg.get("data", msg)
            is_me = data.get("isFromMe", False)
            body = data.get("body", "")
            ts = msg.get("_sent_at", "") or msg.get("_received_at", "") or ""
            sender = data.get("pushName", "") or data.get("notifyName", "")
            chat = data.get("chat", "") or msg.get("chat", "")
            direction = "⬅️ RECV" if not is_me else "➡️ SENT"
            print(f"\n{direction} | {ts[:19]}")
            print(f"   Chat: {chat}")
            print(f"   From: {sender}")
            print(f"   Body: {body}")
        except:
            pass

# 2. Bullet entry
print("\n\n=== BULLET DB ENTRY ===")
with open("C:/nichenexusglobal/bullets_db.json") as f:
    db = json.load(f)
for b in db.get("whatsapp_bullets", []):
    if "vision" in b.get("company", "").lower() or "togo" in b.get("company", "").lower():
        print(json.dumps(b, indent=2, ensure_ascii=False))
        break
else:
    print("(not found in whatsapp_bullets, checking email_bullets...)")
    for b in db.get("email_bullets", []):
        if "vision" in b.get("company", "").lower() or "togo" in b.get("company", "").lower():
            print(json.dumps(b, indent=2, ensure_ascii=False))
            break
    else:
        print("(not found in bullets_db)")
