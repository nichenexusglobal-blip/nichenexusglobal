#!/usr/bin/env python
"""Add Pawa247 Ghana - WhatsApp bullet"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

new = {
    "company": "Pawa247 Technologies",
    "market": "Ghana",
    "segment": "solar_installer",
    "contact_name": "",
    "email": "Registration@pawa247.com",
    "whatsapp": "233266633445",
    "website": "pawa247.site",
    "source": "web_search",
    "verified": True,
    "status": "verified",
    "products_sold": "Solar panels, inverters, batteries, charge controllers, solar accessories. PAYG solar installations.",
    "brands_carried": "Multiple",
    "market_position": "Ghana solar installer, PAYG model. Sales + installation nationwide. WhatsApp primary channel. No portable power stations.",
    "contact_source": "Website: Registration@pawa247.com, +233 266 633 445 (WA)",
    "research_depth": "verified_on_website",
    "research_date": "2026-06-25",
    "notes": "Ghana. Solar installer, not pure distributor. Could resell portable stations as add-on.",
    "sent": False,
    "gate_score": 100,
    "gate_status": "gated"
}

db['whatsapp_bullets'].append(new)
with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

wa_unsent = sum(1 for b in db['whatsapp_bullets'] if not b.get('sent', False) and b.get('whatsapp'))
print(f"Added Pawa247. WA unpaid with valid numbers: {wa_unsent}")
for b in db['whatsapp_bullets']:
    if not b.get('sent', False) and b.get('whatsapp'):
        print(f"  📱 {b['company']} ({b.get('market','?')}) -> {b.get('whatsapp','?')}")
