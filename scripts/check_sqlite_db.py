#!/usr/bin/env python3
"""Check WhatsApp SQLite database for recent messages"""
import sqlite3, os

db_path = 'C:/nichenexusglobal/whatsapp_mail.db'
if not os.path.exists(db_path):
    print(f'DB not found: {db_path}')
    exit(1)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# List tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()
print('Tables:', [t[0] for t in tables])

for t in tables:
    tn = t[0]
    try:
        cur.execute(f"SELECT COUNT(*) FROM [{tn}]")
        count = cur.fetchone()[0]
        print(f'  {tn}: {count} rows')
        
        # Get columns
        cur.execute(f"PRAGMA table_info([{tn}])")
        cols = [c[1] for c in cur.fetchall()]
        print(f'  Columns: {cols[:10]}')
        
        # Show last 5 rows
        if count > 0:
            cur.execute(f"SELECT * FROM [{tn}] ORDER BY rowid DESC LIMIT 5")
            rows = cur.fetchall()
            for r in rows:
                print(f'    {r}')
    except Exception as e:
        print(f'  {tn}: ERROR {e}')

conn.close()
