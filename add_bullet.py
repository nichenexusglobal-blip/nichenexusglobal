#!/usr/bin/env python3
"""Central add-bullet script. Run: python add_bullet.py 'Company Name' market WA email website gate_score"""
import json, sys

with open('bullets_db.json', 'r') as f:
    db = json.load(f)

bullet = {
    "company": "INFLO LTD Malawi",
    "market": "Malawi",
    "segment": "solar_EPC",
    "contact_name": "",
    "email": "info@inflo.mw",
    "whatsapp": "265990098058",
    "website": "inflo.mw",
    "source": "web_search",
    "verified": True,
    "status": "verified",
    "products_sold": "Solar microgrids/minigrids, solar PV systems, power line installation, switchgear, HV/MV/LV distribution. Residential to industrial solutions. Blantyre.",
    "brands_carried": "Multiple",
    "market_position": "Malawi solar and electrical company since 2018. Blantyre-based. Solar microgrids, power lines, switchgear. No portable power stations.",
    "contact_source": "Website: +265 990 098 058, info@inflo.mw, Blantyre Malawi",
    "research_depth": "verified_on_website",
    "research_date": "2026-06-25",
    "notes": "Malawi - very low electrification, frequent blackouts. Solar+electrical company. Phone likely WhatsApp. No portable stations.",
    "gate_score": 80,
    "gate_status": "gated"
}

db["whatsapp_bullets"].append(bullet)
db["last_updated"] = "2026-06-25"

with open('bullets_db.json', 'w') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

wa = db['whatsapp_bullets']
unsent = [b for b in wa if b.get('status') in ('verified','researched') and b.get('sent') != True]
print(f"Added: {bullet['company']} ({bullet['market']})")
print(f"Unsent bullets: {len(unsent)}")
