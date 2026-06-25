#!/usr/bin/env python3
"""Remove dead bullets from bullets_db.json - no contact, no website, unverified."""
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

with open('bullets_db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

dead_companies = {
    # Email bullets - no contact info
    "Otcer.ph",
    "Flexopower Energies",
    "VMI Direct PH",
    "TecAfrica Solutions",
    "Solar Sonic (PTY) Ltd",
    "Fenixx Industrial Power",
    "XO Tech Trading",
    "Mirage Indonesia",
    "Power Station Indonesia",
    "PT. Jevindo Energy Solution",
    "Meta Bee Brasil",
    "EcoFlow Colombia",
    "Jackery Philippines (Techroom)",
    # WhatsApp bullets - no contact
    "Rapidtech Networks Ltd",
    "Starmac Kenya",
    "GrandHub Technologies Ltd",
    "Singaken Kenya Ltd",
    # Tradewheel - no contact, unverified
    "OKE (Nigeria)",
    "BILEME BERACHEL (Nigeria)",
    "Apraku Benjamin (Ghana)",
    "Hassan Aliu (Nigeria)",
    # Alaba - no contact
    "NDC Solar Power Enterprise",
}

before_email = len(db['email_bullets'])
before_wa = len(db['whatsapp_bullets'])

removed_email = [b['company'] for b in db['email_bullets'] if b['company'] in dead_companies]
removed_wa = [b['company'] for b in db['whatsapp_bullets'] if b['company'] in dead_companies]

db['email_bullets'] = [b for b in db['email_bullets'] if b['company'] not in dead_companies]
db['whatsapp_bullets'] = [b for b in db['whatsapp_bullets'] if b['company'] not in dead_companies]

# Update timestamp
from datetime import datetime
db['last_updated'] = datetime.now().strftime('%Y-%m-%d')

with open('bullets_db.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f"✅ bullets_db.json cleaned")
print(f"   Email bullets: {before_email} → {len(db['email_bullets'])}")
print(f"   WhatsApp bullets: {before_wa} → {len(db['whatsapp_bullets'])}")
print(f"   Removed: {len(removed_email)} email + {len(removed_wa)} whatsapp = {len(removed_email)+len(removed_wa)} total")
print()
print("Email removed:")
for c in sorted(removed_email):
    print(f"  - {c}")
print()
print("WhatsApp removed:")
for c in sorted(removed_wa):
    print(f"  - {c}")
