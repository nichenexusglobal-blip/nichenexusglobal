#!/usr/bin/env python
"""Deduplicate bullets_db.json"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

seen = set()
clean = []
for b in db['email_bullets']:
    key = b.get('company','') + b.get('email','')
    if key in seen:
        print(f"DUP REMOVED: {b['company']}")
        continue
    seen.add(key)
    clean.append(b)

db['email_bullets'] = clean

with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

unpaid = [b for b in db['email_bullets'] if not b.get('sent',False) and b.get('company') != 'TURSAN']
print(f"\nClean. Unpaid bullets: {len(unpaid)}")
for b in unpaid:
    print(f"  - {b['company']} ({b.get('market','?')}) -> {b.get('email','?')}")
