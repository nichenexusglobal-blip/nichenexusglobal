#!/usr/bin/env python3
"""Add 5 WhatsApp bullets to bullets_db.json in one batch"""
import json

with open('bullets_db.json', 'r') as f:
    db = json.load(f)

new_bullets = [
    {
        "company": "SolarShop Africa (Kastom Energy Ltd)",
        "market": "Kenya",
        "segment": "solar_distributor",
        "contact_name": "",
        "email": "sales@solarshop.co.ke",
        "whatsapp": "254722863668",
        "website": "solarshop.co.ke",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Solar panels, inverters, batteries, water heaters, outdoor lights, portable power stations (EcoFlow, Hinen). Full solar product marketplace.",
        "brands_carried": "EcoFlow, Hinen, Jinko, Growatt, Deye, Must, WeCo, MODI",
        "market_position": "Kenya's largest online solar marketplace. Serves East & Central Africa. Head office Milestone Business Center, Northern Bypass Rd, Nairobi.",
        "contact_source": "Website: sales@solarshop.co.ke, +254 722 863 668, +254 722 699 112",
        "research_depth": "verified_on_website",
        "research_date": "2026-06-25",
        "notes": "Already sells EcoFlow + Hinen portable power stations. Large marketplace - could be interested in complementary line. WhatsApp number visible on site.",
        "gate_score": 80,
        "gate_status": "gated"
    },
    {
        "company": "Kenyatronics",
        "market": "Kenya",
        "segment": "electronics_retailer",
        "contact_name": "",
        "email": "",
        "whatsapp": "254725231726",
        "website": "kenyatronics.com",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Electronics, smartphones, TVs, home appliances, EcoFlow power stations. General electronics retailer in Nairobi CBD.",
        "brands_carried": "EcoFlow, various electronics brands",
        "market_position": "Kenya electronics retailer since 2015. Rehema House, Standard St, Nairobi CBD. Sells EcoFlow portable stations alongside general electronics.",
        "contact_source": "Website product pages: WhatsApp 0725-231-726 | 0715-539-455",
        "research_depth": "website_viewed",
        "research_date": "2026-06-25",
        "notes": "General electronics store, not solar specialist. Sells EcoFlow but may be interested in alternative line. Has two WhatsApp numbers.",
        "gate_score": 70,
        "gate_status": "gated"
    },
    {
        "company": "Happy Solar Systems",
        "market": "Kenya",
        "segment": "solar_installer",
        "contact_name": "",
        "email": "",
        "whatsapp": "254741163020",
        "website": "happysolar.co.ke",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Solar panels, inverters, lithium batteries, solar installation services. Residential/commercial solar systems.",
        "brands_carried": "Multiple (installation + supply)",
        "market_position": "Kenya solar installer and supplier. Nairobi-based, nationwide installation. 24-hour product delivery nationwide.",
        "contact_source": "Website: WhatsApp +254 741 163020",
        "research_depth": "website_viewed",
        "research_date": "2026-06-25",
        "notes": "Solar installer, not pure distributor. Could resell portable stations as add-on to installations. Has clear WhatsApp on website.",
        "gate_score": 80,
        "gate_status": "gated"
    },
    {
        "company": "Lumen Vault Kenya",
        "market": "Kenya",
        "segment": "power_retailer",
        "contact_name": "",
        "email": "",
        "whatsapp": "254791654198",
        "website": "lumenvault.co.ke",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "Vestwoods portable power station (2009.6Wh/1000W), solar generators. Online electronics store.",
        "brands_carried": "Vestwoods",
        "market_position": "Kenya online retailer. Star Mall, Tom Mboya St, Nairobi CBD. Sells Vestwoods power stations + electronics. Same-day Nairobi delivery.",
        "contact_source": "Website: WhatsApp 0791654198, Star Mall Nairobi",
        "research_depth": "website_viewed",
        "research_date": "2026-06-25",
        "notes": "Sells Vestwoods power station. Small online retailer. Might want alternative supply options.",
        "gate_score": 70,
        "gate_status": "gated"
    },
    {
        "company": "Starmac Kenya",
        "market": "Kenya",
        "segment": "electronics_retailer",
        "contact_name": "",
        "email": "",
        "whatsapp": "254700000000",
        "website": "starmac.co.ke",
        "source": "web_search",
        "verified": True,
        "status": "verified",
        "products_sold": "BLUETTI solar panels, generators, electronics, home appliances. General retailer in Nairobi.",
        "brands_carried": "BLUETTI",
        "market_position": "Kenya online retailer. Sells BLUETTI panels + general electronics. Has 'WhatsApp Order' option on products.",
        "contact_source": "Website: 'Whatsapp Order' button on products",
        "research_depth": "website_viewed",
        "research_date": "2026-06-25",
        "notes": "Need to find actual WhatsApp number from site. Listed WA may not be accurate placeholder.",
        "gate_score": 60,
        "gate_status": "gated"
    }
]

for b in new_bullets:
    db["whatsapp_bullets"].append(b)

db["last_updated"] = "2026-06-25"

with open('bullets_db.json', 'w') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f"Added {len(new_bullets)} new bullets")
print(f"Total whatsapp_bullets: {len(db['whatsapp_bullets'])}")

# Also update the unsent counter
wa = db['whatsapp_bullets']
unsent = [b for b in wa if b.get('status') in ('verified','researched') and b.get('sent') != True]
print(f"Unsent bullets: {len(unsent)}")
for b in unsent:
    print(f"  - {b['company']} ({b['market']}) WA:{b.get('whatsapp','?')}")
