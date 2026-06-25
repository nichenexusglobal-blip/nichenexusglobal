#!/usr/bin/env python3
import json

with open('bullets_db.json', 'r') as f:
    db = json.load(f)

bullet = {
    "company": "Solar Energy Power Sarl (SEP)",
    "market": "Côte d'Ivoire",
    "segment": "solar_installer",
    "contact_name": "",
    "email": "info@energysep.com",
    "whatsapp": "2250507392740",
    "website": "energysep.com",
    "source": "web_search",
    "verified": True,
    "status": "verified",
    "products_sold": "Solar panels (Jinko, LONGi), inverters (Felicity, Huawei), lithium/gel batteries, 500W solar generator, solar water heaters, solar lights, complete PV installation services. Residential and commercial.",
    "brands_carried": "Jinko, LONGi, Felicity, Huawei, Blue Carbon",
    "market_position": "Abidjan-based solar installer and equipment supplier. Founded 2019. Certified by CODINORM and GIZ. Also does solar pumping, hybrid/off-grid systems. Sells 500W solar generator.",
    "contact_source": "GoAfricaOnline: 0507392737/39/40, Website: info@energysep.com, WA: 0507392740",
    "research_depth": "verified_on_website",
    "research_date": "2026-06-25",
    "notes": "Côte d'Ivoire French-speaking market. Already sells 500W solar generator but could benefit from higher-capacity LiFePO4 models (1000Wh+). Has import experience with Tier-1 brands.",
    "gate_score": 85,
    "gate_status": "gated"
}

db["whatsapp_bullets"].append(bullet)
db["last_updated"] = "2026-06-25"

with open('bullets_db.json', 'w') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

wa = db['whatsapp_bullets']
unsent = [b for b in wa if b.get('status') in ('verified','researched') and b.get('sent') != True]
print(f"Added: {bullet['company']}")
print(f"Unsent bullets: {len(unsent)}")
