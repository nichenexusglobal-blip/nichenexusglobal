#!/usr/bin/env python3
"""List fresh WhatsApp bullets (sent=False in DB)"""
import json
with open("C:/nichenexusglobal/bullets_db.json") as f:
    db = json.load(f)
n = 0
for b in db["whatsapp_bullets"]:
    if b.get("sent"):
        continue
    if not b.get("whatsapp"):
        continue
    n += 1
    print(f"  {n}. [{b.get('market','?')}] {b['company']}")
    print(f"     📱 {b['whatsapp']} | {b.get('website','?')}")
    print()
print(f"Fresh: {n}")
