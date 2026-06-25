"""Find Vision Africa messages in SQLite DB"""
import sqlite3, json

db = sqlite3.connect("C:/nichenexusglobal/whatsapp_mail.db")
cur = db.cursor()

# Check all tables
tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Tables:", [t[0] for t in tables])

# Look in messages for Vision Africa
for table in ['messages', 'contact_aliases', 'conversations']:
    if ('messages',) in tables:
        try:
            rows = cur.execute(f"SELECT * FROM {table} WHERE chat_id LIKE '%vision%' OR chat_id LIKE '%2348168510007%' OR content LIKE '%TO-GO%' OR content LIKE '%Vision%'").fetchall()
            if rows:
                print(f"\n{table}: {len(rows)} rows")
                for r in rows[:10]:
                    print(r)
        except:
            rows = cur.execute(f"SELECT * FROM {table}").fetchall()
            print(f"\n{table}: {len(rows)} rows total")

# Search all tables for TO-GO / Vision Africa
for table in ['messages', 'contact_aliases', 'conversations']:
    try:
        for col in ['chat_id', 'contact_name', 'content']:
            rows = cur.execute(f"SELECT * FROM {table} WHERE {col} LIKE '%2348168510007%'").fetchall()
            if rows:
                print(f"\n{table}.{col} LIKE '2348168510007': {len(rows)} rows")
                for r in rows[:5]:
                    print(r)
    except:
        pass

db.close()
