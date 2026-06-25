"""June 23 Follow-up Automation Script"""
import json, subprocess, time

BASE = "C:/nichenexusglobal"

# Follow-up sequence for June 23
# Each: (company, chat_id, draft_key, delay_minutes)
SEQUENCE = [
    # Day 1 send time → 3 days later = 23rd
    ("Detopsy Electrical Shop", "+2349050234845@s.whatsapp.net", "followup", 0),
    ("MacPower (123MacFreys Ltd)", "+2348135503221@s.whatsapp.net", "followup", 3),
    ("Batteriq Kenya", "+254716822014@s.whatsapp.net", "followup2", 3),
    ("Liwal International FZCO", "+971555777305@s.whatsapp.net", "followup", 3),
    ("PowerSafe (EcoFlow Brasil)", "+5511964537343@s.whatsapp.net", "followup", 3),
    ("Monari Agro", "+263787746152@s.whatsapp.net", "followup", 3),
    ("Orifon LTD (Kenya)", "+254714744184@s.whatsapp.net", "followup", 3),
    ("Get Off Grid Zambia", "+260958751872@s.whatsapp.net", "followup", 3),
]

# Load bullets DB
with open(f"{BASE}/bullets_db.json") as f:
    db = json.load(f)

# Build lookup
bullets = {}
for b in db["whatsapp_bullets"]:
    bullets[b["company"]] = b

print("=" * 45)
print("FOLLOW-UP SEQUENCE (DRY RUN)")
print(f"Scheduled: 2026-06-23 10:00")
print("=" * 45)

for company, chat_id, draft_key, delay in SEQUENCE:
    b = bullets.get(company)
    if b and draft_key in b:
        draft = b[draft_key]
        print(f"\n📱 {company}")
        print(f"   Chat: {chat_id}")
        print(f"   Message: {draft[:60]}...")
        if delay > 0:
            print(f"   Delay: {delay} min after previous")
    else:
        print(f"⚠ {company}: no {draft_key} draft found")

print("\n" + "=" * 45)
print("To execute: set send=True in the script")
