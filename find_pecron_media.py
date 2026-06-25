"""Find Pecron-Chris image message ID from SQLite"""
import sqlite3, json

db = sqlite3.connect("C:/nichenexusglobal/whatsapp_mail.db")
cur = db.cursor()

# Search for Pecron messages
rows = cur.execute("SELECT * FROM messages WHERE chat_id LIKE '%208950729404658%' OR chat_id LIKE '%pecron%' OR content LIKE '%Pecron%' OR content LIKE '%Chris%'").fetchall()
print(f"Found {len(rows)} messages")

for r in rows:
    print(f"\nID: {r[0]}")
    print(f"Chat: {r[1]}")
    print(f"Sender: {r[2]}")
    print(f"Content: {str(r[3])[:200]}")
    print(f"Is from me: {r[4]}")
    print(f"Timestamp: {r[6]}")

# Also check messages about Pecron that might have media info
rows2 = cur.execute("""
    SELECT id, chat_id, content, is_from_me, timestamp,
           json_extract(content, '$.message.image') as img,
           json_extract(content, '$.message.video') as vid,
           json_extract(content, '$.message.document') as doc
    FROM messages 
    WHERE chat_id LIKE '%208950729404658%'
""").fetchall()

print(f"\n\n=== Pecron messages with media info ===")
for r in rows2:
    print(f"\nID: {r[0]}, Chat: {r[1]}, is_from_me: {r[4]}")
    print(f"Has image: {bool(r[5])}, Has video: {bool(r[6])}, Has doc: {bool(r[7])}")
    if r[5]:
        print(f"Image data: {str(r[5])[:300]}")

db.close()
