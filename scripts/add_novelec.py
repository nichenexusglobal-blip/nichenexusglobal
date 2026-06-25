#!/usr/bin/env python
"""Add Novelec Ghana - properly researched"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

# Clean up old needs_research entries (Sunny Energy, Kamworks - will be removed)
db['email_bullets'] = [b for b in db['email_bullets'] if b.get('company') not in ('Sunny Energy General Trading LLC', 'Kamworks Ltd', 'Power & Sun')]

# Add Novelec
new = {
    "company": "Novelec Ghana",
    "market": "Ghana",
    "segment": "power_distributor",
    "email": "novelecghana@outlook.com",
    "whatsapp": "233535529622",
    "website": "novelecghana.com",
    "source": "web_search",
    "verified": True,
    "status": "verified",
    "products_sold": "Electrical supplies, generators, power backup solutions, appliances. Wholesale & installation.",
    "brands_carried": "Multiple (electrical brands)",
    "market_position": "Ghana electrical supplies + power generation company. 10+ years. Wholesale + installation. No portable power stations.",
    "contact_source": "Website footer: novelecghana@outlook.com, +233535529622",
    "research_depth": "verified_on_website",
    "research_date": "2026-06-25",
    "notes": "Ghana, Accra. Good match: already sells generators+backup, portable stations are natural add-on.",
    "sent": False,
    "gate_score": 100,
    "gate_status": "gated"
}

db['email_bullets'].append(new)
with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

unpaid = [b for b in db['email_bullets'] if not b.get('sent', False) and b.get('company') != 'TURSAN']
print(f"Added Novelec Ghana. Total unpaid: {len(unpaid)}")
for b in unpaid:
    st = '✅' if b.get('gate_status') == 'gated' else '⏳'
    print(f"  {st} [{b.get('gate_score',0)}] {b['company']} ({b.get('market','?')})")
