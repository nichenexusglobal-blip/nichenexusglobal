import json

db = json.load(open('C:\\nichenexusglobal\\bullets_db.json'))

# Find Genectra
for b in db.get('email_bullets', []):
    if 'enectra' in b.get('company','') or 'enectra' in b.get('email',''):
        print(json.dumps(b, indent=2, ensure_ascii=False))
        break
else:
    print("Genectra not found in email_bullets")
    # List all email bullets
    print("\nAll email bullets:")
    for b in db.get('email_bullets', []):
        print(f"  {b.get('company','?')} | {b.get('email','?')} | status={b.get('status','?')} | sent_date={b.get('sent_date','?')} | replied={b.get('replied','?')}")
