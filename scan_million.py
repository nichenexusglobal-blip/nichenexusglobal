#!/usr/bin/env python3
"""Extract full M Million conversation"""
import json

with open("C:/nichenexusglobal/whatsapp_messages.jsonl") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        if "M Million" not in line and "2349164337200" not in line and "137508176298103" not in line and "million" not in line.lower():
            continue
        try:
            msg = json.loads(line)
            data = msg.get("data", msg)
            is_me = data.get("isFromMe", False)
            body = data.get("body", "")
            ts = msg.get("_sent_at", "") or msg.get("_received_at", "") or data.get("timestamp", "")
            sender = data.get("pushName", "") or data.get("notifyName", "")
            chat = data.get("chat", "") or msg.get("chat", "")
            direction = "⬅️ HIM" if not is_me else "➡️ US"
            print(f"{direction} | {str(ts)[:19]}")
            print(f"   {body[:200]}")
            print()
        except:
            pass

print("=== BULLET DB ===")
with open("C:/nichenexusglobal/bullets_db.json") as f:
    db = json.load(f)
for b in db.get("whatsapp_bullets", []):
    if "million" in b.get("company","").lower():
        print(f"Company: {b.get('company')}")
        print(f"Status: {b.get('status')}")
        print(f"Last reply: {b.get('last_reply')}")
        print(f"Notes: {b.get('notes')}")
        print(f"Draft: {b.get('draft','')[:300]}")
        break
