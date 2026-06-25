#!/usr/bin/env python3
"""Quick review stats for daily review"""
import json

with open('C:/nichenexusglobal/bullets_db.json') as f:
    db = json.load(f)

# Count WhatsApp bullets sent today
wa_sent_today = [b for b in db.get('whatsapp_bullets', []) if b.get('sent_date') == '2026-06-23']
print(f'WhatsApp sent today: {len(wa_sent_today)}')
for b in wa_sent_today:
    ch = b.get('sent_channel', '?')
    print(f'  - {b.get("company")} ({b.get("market")}) via {ch}')

# Count email bullets sent today
email_sent_today = [b for b in db.get('email_bullets', []) if b.get('sent_date') == '2026-06-23']
print(f'Email sent today: {len(email_sent_today)}')
for b in email_sent_today:
    print(f'  - {b.get("company")} ({b.get("market")}): {b.get("email")}')

# Total bullets
print(f'Total email bullets: {len(db.get("email_bullets",[]))}')
print(f'Total whatsapp bullets: {len(db.get("whatsapp_bullets",[]))}')

# Count all sent
email_sent = [b for b in db.get('email_bullets',[]) if b.get('sent')]
wa_sent = [b for b in db.get('whatsapp_bullets',[]) if b.get('sent')]
print(f'Email sent total: {len(email_sent)}')
print(f'WhatsApp sent total: {len(wa_sent)}')

# WhatsApp replies in bullets_db
wa_replied = [b for b in db.get('whatsapp_bullets',[]) if 'reply' in b.get('status','').lower() or 'replied' in b.get('status','').lower()]
print(f'WhatsApp replied: {len(wa_replied)}')
for b in wa_replied:
    print(f'  - {b.get("company")} ({b.get("market")}): {b.get("last_reply","n/a")[:80]}')

# Hammers summary
with open('C:/nichenexusglobal/hammer_db.json') as f:
    hf = json.load(f)
print(f'\nHammer DB: {hf["meta"]["total_hammers"]} hammers, last updated {hf["meta"]["last_updated"]}')
for cat, data in hf['categories'].items():
    verified = sum(1 for h in data.get('hammers',[]) if h.get('source','').startswith('verified'))
    unverified = sum(1 for h in data.get('hammers',[]) if not h.get('source','').startswith('verified'))
    print(f'  {data["name"]}: {len(data.get("hammers",[]))} hammers ({verified} verified, {unverified} unverified)')
