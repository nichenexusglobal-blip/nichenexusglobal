#!/usr/bin/env python
"""Add new verified bullets to DB"""

import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

new = [
    {
        "company": "Emebest Electrical & Solar World",
        "market": "Nigeria",
        "segment": "solar_distributor",
        "email": "",
        "whatsapp": "",
        "website": "emebestsolar.com",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Solar panels, batteries, inverters, controllers, solar street lights, installation services",
        "brands_carried": "Multiple (not specified)",
        "market_position": "Alaba International Market F538, Lagos. Importer and installer of solar+electrical. Nationwide delivery.",
        "contact_source": "Website: contact form only. WhatsApp preferred. RC: 7411950",
        "research_depth": "verified_on_website",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 75,
        "gate_status": "needs_research",
        "gate_issues": ["No email or WhatsApp visible on website", "Products not fully identified"]
    },
    {
        "company": "Yachu Solar Kenya",
        "market": "Kenya",
        "segment": "solar_distributor",
        "email": "Info@yachusolar.com",
        "whatsapp": "254717171915",
        "website": "yachusolar.co.ke",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Lithium batteries, hybrid inverters, solar panels, gel batteries - own factory in Jiangsu China",
        "brands_carried": "Yachu (own brand)",
        "market_position": "Solar distributor with own factory in Jiangsu China. Nairobi CBD shop + Mombasa Rd warehouse. Wholesale & retail.",
        "contact_source": "Website: Info@yachusolar.com, +254 717171915",
        "research_depth": "verified_on_website",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 100,
        "gate_status": "gated"
    },
    {
        "company": "Power & Sun",
        "market": "Kenya",
        "segment": "solar_distributor",
        "email": "",
        "whatsapp": "",
        "website": "powernsun.com",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Solar panels, inverters, batteries, portable power stations - B2B distributor",
        "brands_carried": "Multiple (SMA, Sungrow, Trina, Longi, JA, Dyness, Deye, Pylontech, BYD)",
        "market_position": "Solar B2B distributor Kenya. Sells portable power stations category. Nationwide delivery.",
        "contact_source": "Website: contact form only. Email not published.",
        "research_depth": "website_viewed",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 75,
        "gate_status": "needs_research",
        "gate_issues": ["No email on website", "Contact only via form"]
    }
]

for b in new:
    db['email_bullets'].append(b)
    print(f"ADDED: {b['company']} ({b['market']})")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

unpaid = [b for b in db['email_bullets'] if not b.get('sent', False) and b.get('company') != 'TURSAN']
print(f"\nTotal unpaid: {len(unpaid)}")
for b in unpaid:
    s = b.get('gate_score', 0)
    m = b.get('market', '?')
    e = b.get('email', 'NO EMAIL') or 'NO EMAIL'
    print(f"  [{s}] {b['company']} ({m}) -> {e}")
