#!/usr/bin/env python
"""Add B.Peter Industrial - WhatsApp bullet"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

new = {
    "company": "B.Peter Industrial Tools & Solar",
    "market": "Nigeria",
    "segment": "electrical_solar_distributor",
    "contact_name": "",
    "email": "bperterindustrial@gmail.com",
    "whatsapp": "2348063316412",
    "website": "bpeterindustrialsolar.com",
    "source": "web_search",
    "verified": True,
    "status": "verified",
    "products_sold": "ABB/Schneider/Siemens electrical products, solar panels, inverters, batteries, solar street lights, measuring instruments",
    "brands_carried": "ABB, Schneider, Siemens, CHINT, POSMITH, ENTES",
    "market_position": "F464 F-Line, Alaba International Market, Lagos. Industrial electrical + solar distributor. No portable power stations.",
    "contact_source": "Website: bperterindustrial@gmail.com, +234 806 331 6412",
    "research_depth": "verified_on_website",
    "research_date": "2026-06-25",
    "notes": "Alaba F464. Industrial electric + solar. Strong distribution channel. Portable stations = natural add-on.",
    "sent": False,
    "gate_score": 100,
    "gate_status": "gated"
}

db['whatsapp_bullets'].append(new)
with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

wa_unsent = sum(1 for b in db['whatsapp_bullets'] if not b.get('sent', False))
print(f"Added B.Peter. WA unpaid: {wa_unsent}")
for b in db['whatsapp_bullets']:
    if not b.get('sent', False):
        print(f"  📱 {b['company']} ({b.get('market','?')}) -> {b.get('whatsapp','?')}")
