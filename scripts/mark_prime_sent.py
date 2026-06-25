#!/usr/bin/env python
"""Mark Prime Tech Trading as sent in bullets_db.json"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

for b in db['email_bullets']:
    if b.get('company') == 'Prime Tech Trading (Prime Tech Philippines)':
        b['sent'] = True
        b['sent_date'] = '2026-06-25'
        b['sent_channel'] = 'email'
        b['status'] = 'sent'
        print(f"SUCCESS: {b['company']} marked as sent")
        break

with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)
