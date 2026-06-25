#!/usr/bin/env python
"""Add Naif Falcon - properly researched"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

# Remove old entry
db['email_bullets'] = [b for b in db['email_bullets'] if b.get('company') != 'Naif Falcon Trading (KSA)']

new = {
    "company": "Naif Falcon Trading",
    "market": "UAE / Multi-country (16+ markets)",
    "segment": "solar_distributor",
    "email": "info@naif-falcon.com",
    "whatsapp": "97142299068",
    "website": "naif-falcon.com",
    "source": "web_search",
    "verified": True,
    "status": "verified",
    "products_sold": "Longi/Jinko solar panels, SVOLT lithium batteries, Growatt/Deye inverters, Eastman tubular batteries",
    "brands_carried": "Longi, Jinko, SVOLT, Growatt, Deye, Eastman",
    "market_position": "Dubai-based multi-country distributor. Serves KSA, Nigeria, Egypt, Morocco, Algeria, Pakistan, Zimbabwe, Uganda, Tanzania, Kenya, Oman, Yemen, Iraq, Jordan, Lebanon, Bahrain. No portable power stations.",
    "contact_source": "Website: info@naif-falcon.com, +971 4 229 9068",
    "research_depth": "verified_on_website",
    "research_date": "2026-06-25",
    "notes": "UAE-based, not Saudi. Multi-country reach. No portable power stations. Strong battery/inverter portfolio.",
    "sent": False,
    "gate_score": 100,
    "gate_status": "gated"
}

db['email_bullets'].append(new)
with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f"Added: {new['company']} ({new['market']})")
unpaid = [b for b in db['email_bullets'] if not b.get('sent', False) and b.get('company') != 'TURSAN']
print(f"Total unpaid: {len(unpaid)}")
