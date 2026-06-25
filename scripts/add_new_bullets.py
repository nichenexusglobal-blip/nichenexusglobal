#!/usr/bin/env python
"""Add new bullets (unpaid) to bullets_db.json"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

new_bullets = [
    {
        "company": "ZNC Solar (Zahid & Co.)",
        "market": "Pakistan",
        "segment": "solar_distributor",
        "email": "sales@zncsolar.com",
        "whatsapp": "923348888555",
        "website": "zncsolar.com",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "GoodWe inverters, Soluna lithium batteries - authorized distributor Pakistan",
        "brands_carried": "GoodWe, Soluna",
        "market_position": "Authorized GoodWe/Soluna distributor Pakistan since 1991. Nationwide coverage. No portable power stations in lineup.",
        "contact_source": "Website footer: sales@zncsolar.com, +92 334 8888 555",
        "research_depth": "verified_on_website",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 100,
        "gate_status": "gated"
    },
    {
        "company": "EGreen (Egyptian Renewable Energy Co.)",
        "market": "Egypt",
        "segment": "solar_distributor",
        "email": "sales@egreen-eg.com",
        "whatsapp": "201097770457",
        "website": "egreen-eg.com",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "SOFAR solar inverters, battery storage, solar water heaters",
        "brands_carried": "SOFAR",
        "market_position": "Official SOFAR distributor Egypt. System design, supply, installation. Cairo & Alexandria.",
        "contact_source": "Website: sales@egreen-eg.com, +2 010 9777 0457",
        "research_depth": "verified_on_website",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 100,
        "gate_status": "gated"
    }
]

for b in new_bullets:
    db['email_bullets'].append(b)
    print(f"ADDED: {b['company']}")

# Remove the mistakenly added unpaid EGreen (might be duplicate)
clean = []
for b in db['email_bullets']:
    if b.get('company') == 'EGreen (Egyptian Renewable Energy Co.)' and b.get('sent') == False and 'gate_score' not in b:
        print(f"REMOVED duplicate: {b['company']}")
        continue
    clean.append(b)
db['email_bullets'] = clean

with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

# Show unpaid
unpaid = [b for b in db['email_bullets'] if not b.get('sent', False) and b.get('company') != 'TURSAN']
print(f"\n=== UNPAID BULLETS ({len(unpaid)}) ===")
for b in unpaid:
    print(f"  {b['company']} ({b.get('market', '?')}) -> {b.get('email', '?')}")
