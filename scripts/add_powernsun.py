#!/usr/bin/env python
"""Add Power & Sun - properly researched"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

# Remove the old wrong entry for Power & Sun (Kenya)
db['email_bullets'] = [b for b in db['email_bullets'] if b.get('company') != 'Power & Sun']

# Add corrected entry
new = {
    "company": "Power & Sun (Orange Overseas FZE)",
    "market": "UAE / Global",
    "segment": "solar_distributor",
    "email": "info@powernsun.com",
    "whatsapp": "",
    "website": "powernsun.com",
    "source": "web_search",
    "verified": True,
    "status": "verified",
    "products_sold": "Solar PV modules, inverters (Sungrow/Solis/Deye), BESS, lithium batteries (BYD/Dyness), portable power stations, accessories. 200MW+ aggregate supplies.",
    "brands_carried": "JA Solar, LONGi, Trina, Sungrow, Solis, Deye, SMA, BYD, Dyness, GCL, TW Solar, SAJ, Sunwoda, APAR, Clenergy, Morningstar, Weidmuller, Stäubli",
    "market_position": "UAE FZE, B2B solar distributor. Global supply chain (South Asia, ME, Africa, Europe). Already sells portable power stations. Large wholesaler.",
    "contact_source": "Website: info@powernsun.com. Office: Orange Overseas FZE, UAE.",
    "research_depth": "verified_on_website",
    "research_date": "2026-06-25",
    "notes": "UAE-based, NOT Kenya. Already carries portable power stations. Approach: new brand/line addition for their B2B portfolio.",
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
