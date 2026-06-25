#!/usr/bin/env python
"""Add Davis & Shirtliff + Rex Energy Tanzania"""

import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

new = [
    {
        "company": "Davis & Shirtliff Group",
        "market": "Multi-country Africa",
        "segment": "solar_distributor",
        "email": "ContactCenter@dayliff.com",
        "whatsapp": "254711079000",
        "website": "davisandshirtliff.com",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Diesel generators, solar solutions (panels/inverters/batteries), water pumps, irrigation",
        "brands_carried": "Multiple",
        "market_position": "75-year-old multi-country distributor. 14+ African countries. Generators + solar. No portable power stations.",
        "contact_source": "Website: ContactCenter@dayliff.com, +254 711 079 000",
        "research_depth": "verified_on_website",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 100,
        "gate_status": "gated"
    },
    {
        "company": "Rex Energy Tanzania",
        "market": "Tanzania",
        "segment": "solar_distributor",
        "email": "sales@rexsolarenergy.com",
        "whatsapp": "255712603040",
        "website": "rexsolarenergy.com",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Solar panels, inverters, batteries - solar contractor Tanzania",
        "brands_carried": "Multiple",
        "market_position": "Tanzania's leading solar contractor. 20+ years, 15,000+ projects, 80MW+ installed. Dar es Salaam.",
        "contact_source": "Website: sales@rexsolarenergy.com, info@rexsolarenergy.com, +255 712 603 040",
        "research_depth": "verified_on_website",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 100,
        "gate_status": "gated"
    },
    {
        "company": "AG Energies Co. Ltd",
        "market": "Tanzania",
        "segment": "solar_EPC",
        "email": "info@agenergies.co.tz",
        "whatsapp": "255746022022",
        "website": "agenergies.co.tz",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Solar home systems, PV panels, inverters - EPC and distributor",
        "brands_carried": "Multiple",
        "market_position": "Tanzania EPC solar company. Distributor of solar products. Established 2015. Dar es Salaam + nationwide.",
        "contact_source": "Website: info@agenergies.co.tz, +255-746-022022",
        "research_depth": "verified_on_website",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 100,
        "gate_status": "gated"
    }
]

for b in new:
    db['email_bullets'].append(b)
    print(f"ADDED: {b['company']} ({b['market']})")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

unpaid = [b for b in db['email_bullets'] if not b.get('sent', False) and b.get('company') != 'TURSAN']
print(f"\n=== TOTAL UNPAID: {len(unpaid)} ===")
for b in unpaid:
    s = b.get('gate_score', 0)
    g = b.get('gate_status', '?')
    e = b.get('email', '?') or '?'
    print(f"  [{s}][{g}] {b['company']} ({b.get('market','?')}) -> {e}")
