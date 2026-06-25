#!/usr/bin/env python
"""Mark bullets #5-#8 as sent"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

updates = {
    'Iseli Energy': {'sent': True, 'sent_date': '2026-06-25', 'sent_channel': 'email', 'status': 'sent'},
    'Even Flow Distribution': {'sent': True, 'sent_date': '2026-06-25', 'sent_channel': 'email', 'status': 'sent'},
    'Solarway Suppliers': {'sent': True, 'sent_date': '2026-06-25', 'sent_channel': 'email', 'status': 'sent'},
    'Voltaris Colombia': {'sent': True, 'sent_date': '2026-06-25', 'sent_channel': 'email', 'status': 'sent'}
}

for b in db['email_bullets']:
    name = b.get('company', '')
    if name in updates:
        b.update(updates[name])
        print(f"UPDATED: {name}")

# Also update the duplicate Bluetti entry
for b in db['email_bullets']:
    if b.get('company') == 'Bluetti Philippines (bluettiphilippines.com)':
        b.update({'sent': True, 'sent_date': '2026-06-25', 'sent_channel': 'merged', 'status': 'closed_merged', 'notes': 'Same entity as Prime Tech Trading - emailed via Prime Tech'})
        print(f"UPDATED: {b['company']} (duplicate, merged)")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

# Show remaining unsent email bullets
print("\n=== REMAINING UNSENT (email) ===")
for b in db['email_bullets']:
    if not b.get('sent', False) and b.get('company') != 'TURSAN':
        print(f"- {b['company']} ({b.get('market', '?')}) -> {b.get('email', 'NO EMAIL')}")

print("\n=== REMAINING UNSENT (whatsapp) ===")
for b in db['whatsapp_bullets']:
    if not b.get('sent', False):
        print(f"- {b['company']} ({b.get('market', '?')}) -> WA: {b.get('whatsapp', 'NONE')}")
