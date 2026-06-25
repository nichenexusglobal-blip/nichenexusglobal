#!/usr/bin/env python3
"""Check SQLite DB for today's messages"""
import sqlite3
import os

if not os.path.exists('whatsapp_mail.db'):
    print("whatsapp_mail.db not found")
    exit(1)

conn = sqlite3.connect('whatsapp_mail.db')
cur = conn.cursor()

# Check messages table
cur.execute("SELECT COUNT(*) FROM messages WHERE timestamp LIKE '2026-06-22%'")
cnt = cur.fetchone()[0]
print(f"Today's messages in DB: {cnt}")

cur.execute("SELECT id, chat_id, sender_id, timestamp, body, is_from_me FROM messages WHERE timestamp LIKE '2026-06-22%' LIMIT 20")
rows = cur.fetchall()
for r in rows:
    print(f"  ID={r[0]}, chat={r[1][:30] if r[1] else 'N/A'}, from_me={r[5]}, ts={r[3]}")
    body = str(r[4])[:120] if r[4] else 'N/A'
    print(f"    Body: {body}")
    print()

# Also check conversations
cur.execute("SELECT COUNT(*) FROM conversations")
cnt = cur.fetchone()[0]
print(f"Total conversations: {cnt}")

# Check for auto-reply chats (LID-based) to filter
cur.execute("SELECT DISTINCT chat_id FROM messages WHERE is_from_me=0 AND timestamp LIKE '2026-06-22%'")
rows = cur.fetchall()
print(f"\nChats with incoming messages today:")
for r in rows:
    print(f"  {r[0]}")

conn.close()
