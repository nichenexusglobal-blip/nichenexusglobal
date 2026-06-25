#!/usr/bin/env python
"""Add verified leads with emails"""

import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

new = [
    {
        "company": "X Flo Energy",
        "market": "Zambia",
        "segment": "solar_distributor",
        "email": "sales@xfloenergy.com",
        "whatsapp": "260976726811",
        "website": "xfloenergy.com",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Hybrid energy solutions, solar, battery storage - serving Africa",
        "brands_carried": "Multiple",
        "market_position": "Energy solutions provider Zambia. Hybrid/solar/storage for African market.",
        "contact_source": "Website: info@xfloenergy.com, sales@xfloenergy.com, +260 97 672 6811",
        "research_depth": "website_viewed",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 100,
        "gate_status": "gated"
    },
    {
        "company": "Eco-Fluxo",
        "market": "Angola",
        "segment": "solar_installer",
        "email": "Geral@ecofluxo.ao",
        "whatsapp": "244936426188",
        "website": "ecofluxo.ao",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Solar photovoltaic systems, off-grid residential systems - Angola",
        "brands_carried": "",
        "market_position": "Angola solar solutions company. Residential/commercial off-grid systems. Luanda.",
        "contact_source": "LinkedIn: Geral@ecofluxo.ao, +244 936 426 188",
        "research_depth": "website_viewed",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 100,
        "gate_status": "gated"
    },
    {
        "company": "Sunny Energy General Trading LLC",
        "market": "UAE/Dubai",
        "segment": "solar_distributor",
        "email": "",
        "whatsapp": "971528574670",
        "website": "sunnyenergyco.com",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Solis inverters, Dyness batteries, BLUETTI power stations, solar panels - distributor",
        "brands_carried": "Solis, Dyness, BLUETTI",
        "market_position": "Dubai-based distributor. Solis inverters, Dyness batteries, BLUETTI stations. Serves UAE, Middle East, Africa.",
        "contact_source": "Website: +971 52 857 4670. Email not published on site.",
        "research_depth": "verified_on_website",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 75,
        "gate_status": "needs_research",
        "gate_issues": ["No email on website", "Already sells BLUETTI - existing supplier"]
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
    m = b.get('market', '?')
    e = b.get('email', '?') or '?'
    print(f"  [{s}] {b['company']} ({m}) -> {e}")
