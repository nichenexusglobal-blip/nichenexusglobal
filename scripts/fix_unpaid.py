#!/usr/bin/env python
"""Fix ZNC Solar - mark as unpaid. Also add EGreen as unpaid if needed."""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

# Fix ZNC - should be unpaid
for b in db['email_bullets']:
    if b.get('company') == 'ZNC Solar (Zahid & Co.)':
        b['sent'] = False
        b['status'] = 'verified'
        del b['sent_date']
        del b['sent_channel']
        print(f"FIXED: ZNC Solar -> unpaid")
    if b.get('company') == 'EGreen (Egyptian Renewable Energy Co.)':
        b['sent'] = False
        b['status'] = 'verified'
        del b['sent_date']
        del b['sent_channel']
        print(f"FIXED: EGreen -> unpaid")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

# Show unpaid count
unpaid = [b for b in db['email_bullets'] if not b.get('sent', False)]
print(f"\nTotal unpaid email bullets: {len(unpaid)}")
for b in unpaid:
    print(f"  - {b['company']} ({b.get('market', '?')}) -> {b.get('email', '?')}")
