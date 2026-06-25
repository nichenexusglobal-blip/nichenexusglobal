#!/usr/bin/env python
"""Add Capslock Thailand bullet"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

new = {
    "company": "Capslock Co. Ltd (ThailandUPS)",
    "market": "Thailand",
    "segment": "power_station",
    "email": "info@capslockthai.com",
    "whatsapp": "",
    "website": "thailandups.com",
    "source": "web_search",
    "verified": True,
    "status": "verified",
    "products_sold": "Jackery power stations (Explorer 1000 Pro 1002Wh/1000W 29,800THB, Explorer 300 Plus 288Wh/300W 11,100THB), SolarSaga panels",
    "brands_carried": "Jackery",
    "market_position": "Official Jackery distributor Thailand. Retail/online. Nonthaburi.",
    "contact_source": "Website: info@capslockthai.com, Tel 0 2952 7824",
    "research_depth": "verified_on_website",
    "research_date": "2026-06-25",
    "sent": False,
    "gate_score": 100,
    "gate_status": "gated"
}

db['email_bullets'].append(new)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

unpaid = [b for b in db['email_bullets'] if not b.get('sent', False) and b.get('company') != 'TURSAN']
print(f"Added. Unpaid: {len(unpaid)}")
for b in unpaid:
    print(f"  {b['company']} ({b.get('market','?')}) -> {b.get('email','?')}")
