#!/usr/bin/env python
"""Add NDC Solar Power - WhatsApp bullet"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

new = {
    "company": "NDC Solar Power Enterprise",
    "market": "Nigeria",
    "segment": "solar_distributor",
    "contact_name": "",
    "email": "info@ndcsolarpower.com",
    "whatsapp": "2347046073559",
    "website": "ndcsolarpower.com",
    "source": "web_search",
    "verified": True,
    "status": "verified",
    "products_sold": "Solar panels, inverters, batteries, solar charge controllers, solar accessories, complete solar kits",
    "brands_carried": "Multiple",
    "market_position": "Alaba International Market F394B, Lagos. Solar equipment distributor. No portable power stations. 24/7 WhatsApp support.",
    "contact_source": "Website: info@ndcsolarpower.com, +234 7046073559, RC: 6996231",
    "research_depth": "verified_on_website",
    "research_date": "2026-06-25",
    "notes": "Alaba F394B. Sells solar components only - no portable power stations. Has email + WA. WhatsApp-first business.",
    "sent": False,
    "gate_score": 100,
    "gate_status": "gated"
}

db['whatsapp_bullets'].append(new)
with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

wa_count = len(db['whatsapp_bullets'])
wa_unsent = sum(1 for b in db['whatsapp_bullets'] if not b.get('sent', False))
print(f"Added NDC Solar. WhatsApp bullets: {wa_unsent}/{wa_count} unpaid")
for b in db['whatsapp_bullets']:
    if not b.get('sent', False):
        print(f"  📱 [{b.get('gate_score',0)}] {b['company']} ({b.get('market','?')}) -> {b.get('whatsapp', '?')}")
