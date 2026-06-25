#!/usr/bin/env python
"""Add Naif Falcon Saudi Arabia bullet"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

new = {
    "company": "Naif Falcon Trading (KSA)",
    "market": "Saudi Arabia",
    "segment": "solar_distributor",
    "email": "",
    "whatsapp": "",
    "website": "naif-falcon.com",
    "source": "web_search",
    "verified": True,
    "status": "verified",
    "products_sold": "Longi solar panels, SVOLT lithium batteries, Growatt/Deye inverters - authorized distributor KSA",
    "brands_carried": "Longi, SVOLT, Growatt, Deye, Eastman",
    "market_position": "Authorized distributor of multiple solar brands in Saudi Arabia. Also UAE office. Strong battery/inverter portfolio but no portable power stations.",
    "contact_source": "Website: contact form only. Need deeper research for email/WA.",
    "research_depth": "website_viewed",
    "research_date": "2026-06-25",
    "sent": False,
    "gate_score": 75,
    "gate_status": "needs_research",
    "gate_issues": ["No email or WhatsApp found on website", "Market position verified"]
}

db['email_bullets'].append(new)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

unpaid = [b for b in db['email_bullets'] if not b.get('sent', False) and b.get('company') != 'TURSAN']
print(f"Added. Unpaid: {len(unpaid)}")
for b in unpaid:
    score = b.get('gate_score', 0)
    status = b.get('gate_status', '?')
    email = b.get('email', 'NO EMAIL') or 'NO EMAIL'
    print(f"  [{score}/100] {b['company']} ({b.get('market','?')}) -> {email} [{status}]")
