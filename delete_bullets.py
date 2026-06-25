#!/usr/bin/env python3
import json

with open('bullets_db.json', 'r') as f:
    db = json.load(f)

remove = [
    'LTE Groupe (Lamine Traoré Entreprise)',
    'Freshtec Energy Zambia', 
    'ABT Global Ventures Ltd',
    'Solar King'
]

before = len(db['whatsapp_bullets'])
db['whatsapp_bullets'] = [b for b in db['whatsapp_bullets'] if b['company'] not in remove]
after = len(db['whatsapp_bullets'])

removed_count = before - after
unsent = [b for b in db['whatsapp_bullets'] if b.get('status') in ('verified','researched') and b.get('sent') != True]

print(f"Removed: {removed_count} bullets")
print(f"Total whatsapp_bullets: {after}")
print(f"Remaining unsent: {len(unsent)}")
for b in unsent:
    print(f"  - {b['company']} ({b['market']}) WA:{b.get('whatsapp','?')}")

db['last_updated'] = '2026-06-25'
with open('bullets_db.json', 'w') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)
