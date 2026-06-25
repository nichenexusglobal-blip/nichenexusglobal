#!/usr/bin/env python3
"""Check contact aliases and TO-GO conversation details"""
import sqlite3

conn = sqlite3.connect('C:/nichenexusglobal/whatsapp_mail.db')
c = conn.cursor()

# Check contact_aliases table
c.execute("SELECT * FROM contact_aliases LIMIT 20")
aliases = c.fetchall()
print("=== Contact Aliases ===")
for a in aliases:
    print(f"  {a}")

# Check conversations
c.execute("SELECT * FROM conversations LIMIT 10")
convos = c.fetchall()
print("\n=== Conversations ===")
for co in convos:
    print(f"  {co}")

# Full TO-GO conversation: 196795552559324@lid
print("\n\n=== Full TO-GO Conversation (196795552559324@lid) ===")
c.execute("""
    SELECT datetime(timestamp, 'unixepoch', '+8 hours') as ts, 
           is_from_me, body
    FROM messages 
    WHERE chat_id = '196795552559324@lid'
    ORDER BY timestamp ASC
""")
for ts, is_from, body in c.fetchall():
    who = "US >>>" if is_from else "<<< THEM"
    print(f"  [{ts}] {who}")
    print(f"    {body[:200]}")
    print()

conn.close()
