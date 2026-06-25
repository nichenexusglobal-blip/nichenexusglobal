#!/usr/bin/env python3
"""Check WhatsApp SQLite database for incoming messages"""
import sqlite3

conn = sqlite3.connect('C:/nichenexusglobal/whatsapp_mail.db')
c = conn.cursor()

# Get tables
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in c.fetchall()]
print(f"Tables: {tables}")

if 'messages' in tables:
    c.execute('PRAGMA table_info(messages)')
    cols = c.fetchall()
    print(f"Columns: {[col[1] for col in cols]}")
    
    # Total counts
    c.execute('SELECT COUNT(*) FROM messages')
    total = c.fetchone()[0]
    print(f"\nTotal messages: {total}")
    
    c.execute("SELECT COUNT(*) FROM messages WHERE is_from_me=0")
    incoming = c.fetchone()[0]
    print(f"Incoming (not from us): {incoming}")
    
    c.execute("SELECT COUNT(*) FROM messages WHERE is_from_me=1")
    outgoing = c.fetchone()[0]
    print(f"Outgoing (from us): {outgoing}")
    
    # Recent incoming messages - last 15
    print("\n=== Recent incoming messages (last 15) ===")
    c.execute("""
        SELECT datetime(timestamp, 'unixepoch', '+8 hours') as ts, 
               chat_id, substr(body,1,120) as body_preview 
        FROM messages WHERE is_from_me=0 
        ORDER BY timestamp DESC LIMIT 15
    """)
    for ts, chat, body in c.fetchall():
        print(f"  [{ts}] {chat}: {body}")
    
    # All messages today (UTC+8)
    print("\n=== Messages today (2026-06-23, UTC+8) ===")
    c.execute("""
        SELECT datetime(timestamp, 'unixepoch', '+8 hours') as ts, 
               chat_id, is_from_me, substr(body,1,120) as body_preview
        FROM messages 
        WHERE datetime(timestamp, 'unixepoch', '+8 hours') >= '2026-06-23 00:00:00'
        ORDER BY timestamp DESC LIMIT 30
    """)
    msgs = c.fetchall()
    if msgs:
        for ts, chat, fm, body in msgs:
            who = "OUT" if fm else "IN"
            print(f"  [{ts}] {who} {chat}: {body}")
    else:
        print("  (no messages today)")
    
    # Get distinct chat IDs
    print("\n=== Unique chat conversations ===")
    c.execute("""
        SELECT chat_id, COUNT(*) as cnt, MAX(timestamp) as last 
        FROM messages 
        GROUP BY chat_id 
        ORDER BY last DESC LIMIT 10
    """)
    for chat, cnt, last in c.fetchall():
        import datetime
        ts = datetime.datetime.fromtimestamp(last, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
        print(f"  {chat}: {cnt} msgs, last {ts}")
else:
    print("No 'messages' table found")
    for t in tables:
        c.execute(f'SELECT * FROM "{t}" LIMIT 3')
        rows = c.fetchall()
        print(f"\nTable {t}: {rows}")

conn.close()
