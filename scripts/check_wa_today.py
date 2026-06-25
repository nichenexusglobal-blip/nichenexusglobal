#!/usr/bin/env python3
"""Check WhatsApp messages from today from all sources"""
import json

# 1. Check JSONL file
print("=== WHATSAPP JSONL (today June 22) ===")
count = 0
with open('whatsapp_messages.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            obj = json.loads(line)
            ts = obj.get('timestamp', str(obj))
            if '2026-06-22' in str(ts):
                event = obj.get('event', obj.get('type', 'unknown'))
                data = obj.get('data', {})
                is_from_me = data.get('isFromMe', obj.get('isFromMe', True))
                chat = data.get('chat', obj.get('chatId', ''))
                sender = data.get('sender', obj.get('from', ''))
                body = data.get('body', obj.get('message', ''))
                # Skip internal messages
                print(f"  Event: {event}")
                print(f"  isFromMe: {is_from_me}")
                print(f"  Chat: {chat}")
                print(f"  Sender: {sender}")
                print(f"  Body: {str(body)[:200]}")
                print()
                count += 1
        except:
            pass

print(f"Total June 22 entries: {count}")

# 2. Check SQLite database
import sqlite3
import os
if os.path.exists('whatsapp_mail.db'):
    conn = sqlite3.connect('whatsapp_mail.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    print(f"\n=== SQLite DB Tables ===")
    for t in tables:
        print(f"  Table: {t[0]}")
    # Count today's messages
    for t in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM \"{t[0]}\" WHERE timestamp LIKE '2026-06-22%'")
            cnt = cur.fetchone()[0]
            if cnt > 0:
                cur.execute(f"SELECT * FROM \"{t[0]}\" WHERE timestamp LIKE '2026-06-22%' LIMIT 5")
                rows = cur.fetchall()
                print(f"\n  Today's in {t[0]}: {cnt}")
                for r in rows:
                    print(f"    {r}")
        except:
            pass
    conn.close()
else:
    print("\n=== SQLite DB: not found ===")
