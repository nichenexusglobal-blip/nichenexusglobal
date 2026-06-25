#!/usr/bin/env python3
"""Scan whatsapp_messages.jsonl for all conversations"""
import json
from collections import defaultdict

messages = []
with open("C:/nichenexusglobal/whatsapp_messages.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            try:
                messages.append(json.loads(line))
            except:
                pass

conversations = defaultdict(list)
for msg in messages:
    chat = msg.get("data", {}).get("chat", "") or msg.get("chat", "")
    if not chat:
        continue
    conversations[chat].append(msg)

print(f"Total records: {len(messages)}")
print(f"Unique conversations: {len(conversations)}")
print()

# Display each conversation
for chat, msgs in sorted(conversations.items()):
    name = "?"
    for m in msgs:
        n = m.get("data", {}).get("pushName", "") or m.get("data", {}).get("notifyName", "") or ""
        if n:
            name = n
            break
    
    sent = [m for m in msgs if m.get("data", {}).get("isFromMe", False) or m.get("isFromMe", False)]
    recv = [m for m in msgs if not (m.get("data", {}).get("isFromMe", False) or m.get("isFromMe", False))]
    
    phone = chat.split("@")[0]
    
    print(f"📱 {phone} | {name}")
    
    if sent:
        last_s = sent[-1]
        body_s = last_s.get("data", {}).get("body", "") or last_s.get("body", "")
        ts_s = last_s.get("_sent_at", "")[:16] or ""
        print(f"   ➡️  Sent {len(sent)}x | Last: {ts_s}")
        print(f"      \"{body_s[:80]}\"")
    
    if recv:
        last_r = recv[-1]
        body_r = last_r.get("data", {}).get("body", "") or last_r.get("body", "")
        ts_r = last_r.get("_received_at", "")[:16] or ""
        print(f"   ⬅️  Recv {len(recv)}x | Last: {ts_r}")
        print(f"      \"{body_r[:100]}\"")
    
    print()
