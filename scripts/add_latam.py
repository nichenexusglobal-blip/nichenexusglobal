#!/usr/bin/env python
"""Add Latin America bullets"""

import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

new = [
    {
        "company": "Powerstein Mexico",
        "market": "Mexico",
        "segment": "power_station",
        "email": "ventas@powersteindf.mx",
        "whatsapp": "525525956358",
        "website": "powersteindf.mx",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "EcoFlow DELTA/RIVER power stations, solar panels, portable batteries",
        "brands_carried": "EcoFlow",
        "market_position": "Mexico City-based EcoFlow retailer. Sells portable power stations, batteries, solar panels.",
        "contact_source": "Website: ventas@powersteindf.mx, (+52) 55 2595 6358",
        "research_depth": "verified_on_website",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 100,
        "gate_status": "gated"
    },
    {
        "company": "Venta Solar Peru",
        "market": "Peru",
        "segment": "solar_retailer",
        "email": "ventas@ventasolarperu.com",
        "whatsapp": "51991711057",
        "website": "ventasolarperu.com",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Solar panels, batteries, inverters, solar energy systems",
        "brands_carried": "Multiple",
        "market_position": "Peru solar equipment distributor. Lima-based. Sells panels, batteries, inverters nationwide.",
        "contact_source": "Website: ventas@ventasolarperu.com, +51 991 711 057",
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
gated = [b for b in unpaid if b.get('gate_status') == 'gated']
print(f"Gated (ready to send): {len(gated)}")
print(f"Need research: {len(unpaid) - len(gated)}")
for b in unpaid:
    print(f"  [{b.get('gate_score',0)}] {b['company']} ({b.get('market','?')})")
