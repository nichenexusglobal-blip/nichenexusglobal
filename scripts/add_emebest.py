#!/usr/bin/env python
"""Add Emebest - properly researched"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

# Remove old entry if exists
db['email_bullets'] = [b for b in db['email_bullets'] if b.get('company') != 'Emebest Electrical & Solar World']

new = {
    "company": "Emebest Electrical & Solar World",
    "market": "Nigeria",
    "segment": "solar_importer",
    "email": "emebestsolar@gmail.com",
    "whatsapp": "2347069981764",
    "website": "emebestsolar.com",
    "source": "web_search",
    "verified": True,
    "status": "verified",
    "products_sold": "Solar panels, lithium batteries (Li-Ion/AGM/GEL), inverters, controllers, solar street lights, installation services",
    "brands_carried": "Multiple (direct importer)",
    "market_position": "Alaba International Market F538, Lagos. Direct importer of solar+electrical. Nationwide delivery + installation. No portable power stations.",
    "contact_source": "Website footer: emebestsolar@gmail.com, 0706 998 1764",
    "research_depth": "verified_on_website",
    "research_date": "2026-06-25",
    "notes": "Alaba F538. Direct importer. Sells batteries but not portable power stations. Natural extension for their product line.",
    "sent": False,
    "gate_score": 100,
    "gate_status": "gated"
}

db['email_bullets'].append(new)
with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f"Added: {new['company']}")
unpaid = [b for b in db['email_bullets'] if not b.get('sent', False) and b.get('company') != 'TURSAN']
print(f"Total unpaid: {len(unpaid)}")
