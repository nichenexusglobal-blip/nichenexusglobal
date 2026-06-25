#!/usr/bin/env python
"""Add new verified bullets: Philippines, Vietnam, Cambodia"""

import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

new = [
    {
        "company": "Solarix Enterprise",
        "market": "Philippines",
        "segment": "solar_distributor",
        "email": "sales@solarixph.com",
        "whatsapp": "639615490780",
        "website": "solarixph.com",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Solar generators, solar panels, inverters - residential/commercial solar systems",
        "brands_carried": "Multiple",
        "market_position": "Philippines solar company. Design, supply, installation. Sells solar generators. Angeles City.",
        "contact_source": "Website: sales@solarixph.com, (632) 8237-1355",
        "research_depth": "verified_on_website",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 100,
        "gate_status": "gated"
    },
    {
        "company": "EGE Cambodia Energy Solutions",
        "market": "Cambodia",
        "segment": "solar_EPC",
        "email": "info@egecambodia.com",
        "whatsapp": "85578256088",
        "website": "egecambodia.com",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Solar energy systems, project management, installation & maintenance",
        "brands_carried": "Multiple",
        "market_position": "Cambodia solar EPC company. Feasibility, design, installation, maintenance. Phnom Penh.",
        "contact_source": "Website: info@egecambodia.com, 078 256 088 / 012 256 068",
        "research_depth": "verified_on_website",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 100,
        "gate_status": "gated"
    },
    {
        "company": "Myanmar Eco Solutions",
        "market": "Myanmar",
        "segment": "solar_EPC",
        "email": "info@myanmarecosolutions.com",
        "whatsapp": "959406196190",
        "website": "myanmarecosolutions.com",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Solar products, renewable energy solutions - product sourcing to project implementation",
        "brands_carried": "Multiple",
        "market_position": "Myanmar renewable energy company. End-to-end solar services. Yangon.",
        "contact_source": "Website: info@myanmarecosolutions.com, +95 9 40 619 619 0-1",
        "research_depth": "verified_on_website",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 100,
        "gate_status": "gated"
    },
    {
        "company": "Kamworks Ltd",
        "market": "Cambodia",
        "segment": "solar_EPC",
        "email": "",
        "whatsapp": "",
        "website": "kamworks.com",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Solar project EPC - feasibility, design, installation, O&M. Commercial/industrial solar.",
        "brands_carried": "Multiple (European tech focus)",
        "market_position": "Leading solar EPC Cambodia. Founded 2006 by Dutch engineers. Large commercial projects.",
        "contact_source": "Website: contact form only. Email not published.",
        "research_depth": "website_viewed",
        "research_date": "2026-06-25",
        "sent": False,
        "gate_score": 75,
        "gate_status": "needs_research",
        "gate_issues": ["No email on website", "EPC focused, may not distribute products"]
    }
]

for b in new:
    db['email_bullets'].append(b)
    print(f"ADDED: {b['company']} ({b['market']})")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

unpaid = [b for b in db['email_bullets'] if not b.get('sent', False) and b.get('company') != 'TURSAN']
gated = [b for b in unpaid if b.get('gate_status') == 'gated']
print(f"\nTotal unpaid: {len(unpaid)} (gated: {len(gated)}, need research: {len(unpaid)-len(gated)})")
for b in unpaid:
    print(f"  [{b.get('gate_score',0)}] {b['company']} ({b.get('market','?')})")
