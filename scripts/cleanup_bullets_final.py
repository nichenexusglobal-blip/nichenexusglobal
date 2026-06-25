#!/usr/bin/env python
"""Final cleanup: mark Power Solution Mall as sent, show final stats"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

# Fix Power Solution Mall - was actually sent via WA on June 19
for b in db['email_bullets']:
    if b.get('company') == 'Power Solution Mall':
        b['sent'] = True
        b['sent_date'] = '2026-06-19'
        b['sent_channel'] = 'whatsapp'
        b['status'] = 'sent'
        b['notes'] = 'Sent via WhatsApp June 19 (Pen approved). DB not updated until June 25 cleanup.'
        print(f"FIXED: {b['company']} - marked sent (was already sent)")

# Stats
email_total = len(db['email_bullets'])
email_sent = sum(1 for b in db['email_bullets'] if b.get('sent', False) or b.get('status') == 'sent')
whatsapp_total = len(db['whatsapp_bullets'])
whatsapp_sent = sum(1 for b in db['whatsapp_bullets'] if b.get('sent', False) or b.get('status').startswith('sent') or b.get('status').startswith('replied') or b.get('status') in ('contacted', 'closed_no_followup'))

print(f"\n=== FINAL STATS ===")
print(f"Email bullets: {email_sent}/{email_total} sent")
print(f"WhatsApp bullets: {whatsapp_sent}/{whatsapp_total} processed")

# Show truly unsent with contact info
print(f"\n=== TRULY UNSENT ===")
unc = 0
for b in db['email_bullets']:
    if not b.get('sent', False) and b.get('email'):
        print(f"  {b['company']} - {b['email']}")
        unc += 1
for b in db['whatsapp_bullets']:
    if not b.get('sent', False) and b.get('whatsapp'):
        print(f"  {b['company']} - WA: {b['whatsapp']}")
        unc += 1
if unc == 0:
    print("  (none - bullet library is clear!)")
else:
    print(f"  Total: {unc} unsent with contact info")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)
print("\nDatabase updated.")
