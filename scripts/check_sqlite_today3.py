#!/usr/bin/env python3
"""Check all timestamps in SQLite for today's dates"""
import sqlite3
from datetime import datetime, timezone, timedelta

conn = sqlite3.connect('whatsapp_mail.db')
cur = conn.cursor()

# Check what dates/format exist
cur.execute("SELECT created_at, timestamp FROM messages ORDER BY timestamp DESC LIMIT 10")
rows = cur.fetchall()
print("=== Last 10 messages dates ===")
for r in rows:
    print(f"  created_at={r[0]}, timestamp={r[1]}")

# Check if timestamp is unix epoch
cur.execute("SELECT created_at FROM messages ORDER BY timestamp DESC LIMIT 1")
latest = cur.fetchone()
if latest:
    print(f"\nLatest created_at: {latest[0]}")

# Try to interpret timestamp as epoch
if rows[0][1]:
    ts = float(rows[0][1])
    dt = datetime.fromtimestamp(ts, tz=timezone(timedelta(hours=8)))
    print(f"Latest message timestamp as datetime: {dt}")

# Query using created_at string
cur.execute("SELECT COUNT(*) FROM messages WHERE created_at LIKE '%2026-06-22%'")
cnt = cur.fetchone()[0]
print(f"\nMessages with created_at containing 2026-06-22: {cnt}")

# Query all recent created_at values
cur.execute("SELECT created_at FROM messages ORDER BY created_at DESC LIMIT 20")
rows = cur.fetchall()
print("\n=== All recent created_at values ===")
for r in rows:
    print(f"  {r[0]}")

conn.close()
