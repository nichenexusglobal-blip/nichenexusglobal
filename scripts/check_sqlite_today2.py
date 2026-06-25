#!/usr/bin/env python3
"""Check SQLite DB schema and today's messages"""
import sqlite3

conn = sqlite3.connect('whatsapp_mail.db')
cur = conn.cursor()

# Check schema
cur.execute("PRAGMA table_info(messages)")
cols = cur.fetchall()
print("=== messages schema ===")
for c in cols:
    print(f"  {c}")

# Try alternate query
cur.execute("SELECT * FROM messages WHERE timestamp LIKE '2026-06-22%' LIMIT 5")
rows = cur.fetchall()
print(f"\n=== Today's messages: {len(rows)} ===")
for r in rows:
    print(f"  {r}")

# Check all rows count
cur.execute("SELECT COUNT(*) FROM messages")
cnt = cur.fetchone()[0]
print(f"\nTotal messages: {cnt}")

conn.close()
