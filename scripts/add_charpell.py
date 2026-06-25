#!/usr/bin/env python
"""Add Charpell Inverter & Solar - WhatsApp bullet"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

new = {
    "company": "Charpell Inverter & Solar Energy",
    "market": "Nigeria",
    "segment": "solar_retailer",
    "contact_name": "",
    "email": "charpellumeh@gmail.com",
    "whatsapp": "2348066098146",
    "website": "",
    "source": "web_search",
    "verified": True,
    "status": "verified",
    "products_sold": "Batteries, inverters, solar energy products for homes and offices",
    "brands_carried": "",
    "market_position": "H120, Alaba International Market, Lagos. Solar inverter & battery dealer. No portable power stations.",
    "contact_source": "Finelib listing: charpellumeh@gmail.com, 0806 609 8146",
    "research_depth": "website_viewed",
    "research_date": "2026-06-25",
    "notes": "Alaba H120. Sells inverters+batteries. No portable stations.",
    "sent": False,
    "gate_score": 100,
    "gate_status": "gated"
}

db['whatsapp_bullets'].append(new)
with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

wa_unsent = sum(1 for b in db['whatsapp_bullets'] if not b.get('sent', False) and b.get('whatsapp'))
print(f"Added Charpell. WA bullets with valid numbers: {wa_unsent}")
for b in db['whatsapp_bullets']:
    if not b.get('sent', False) and b.get('whatsapp'):
        print(f"  📱 {b['company']} ({b.get('market','?')}) -> {b.get('whatsapp','?')}")
