#!/usr/bin/env python
"""Mark bullets as sent in bullets_db.json"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

updates = {
    'Bluetti Philippines (bluettiphilippines.com)': {
        'sent': True, 'sent_date': '2026-06-25', 'sent_channel': 'merged',
        'status': 'closed_merged', 'notes': 'Same entity as Prime Tech Trading (primetechtrading.ph). Emailed via Prime Tech.'
    },
    'Bluetti PH (bluettipower.ph)': {
        'sent': True, 'sent_date': '2026-06-25', 'sent_channel': 'email',
        'status': 'sent'
    }
}

for b in db['email_bullets']:
    name = b.get('company', '')
    if name in updates:
        b.update(updates[name])
        print(f"UPDATED: {name}")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print("DONE")
