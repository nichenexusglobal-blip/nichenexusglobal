import json

db = json.load(open('C:\\nichenexusglobal\\bullets_db.json'))
eb = db.get('email_bullets', [])
wb = db.get('whatsapp_bullets', [])

# Find all replied bullets
print("=== REPLIED BULLETS ===")
for b in eb + wb:
    if b.get('replied') == True or b.get('status') == 'replied':
        print(f"{b.get('company','?')} | {b.get('email','') or b.get('whatsapp','')} | replied: {b.get('replied','?')} | status: {b.get('status','?')} | last_reply: {b.get('last_reply','N/A')} | sent_date: {b.get('sent_date','N/A')}")

print("\n=== WAITING REPLY (sent but not replied) ===")
for b in eb + wb:
    if b.get('status') == 'sent' and not b.get('replied'):
        print(f"{b.get('company','?')} | {b.get('email','') or b.get('whatsapp','')} | last_reply: {b.get('last_reply','N/A')} | sent_date: {b.get('sent_date','N/A')}")
