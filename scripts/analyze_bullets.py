import json

with open('C:\\nichenexusglobal\\bullets_db.json', 'r') as f:
    db = json.load(f)

email_bullets = db.get('email_bullets', [])
whatsapp_bullets = db.get('whatsapp_bullets', [])

# Today's sent (2026-06-24)
today_sent_email = [b for b in email_bullets if b.get('sent_date') == '2026-06-24']
today_sent_wa = [b for b in whatsapp_bullets if b.get('last_sent','').startswith('2026-06-24') or b.get('sent_date') == '2026-06-24']

print('=== TODAY SENT EMAIL ===')
for b in today_sent_email:
    print(f"{b.get('company','?')} | {b.get('email','?')} | replied: {b.get('replied','?')} | last_reply: {b.get('last_reply','N/A')} | gate_score: {b.get('gate_score','?')}")

print()
print('=== TODAY SENT WHATSAPP ===')
for b in today_sent_wa:
    print(f"{b.get('company','?')} | {b.get('whatsapp','?')} | replied: {b.get('replied','?')} | last_reply: {b.get('last_reply','N/A')} | gate_score: {b.get('gate_score','?')}")

# Overall stats
total_email = len(email_bullets)
total_wa = len(whatsapp_bullets)

sent = [b for b in email_bullets+whatsapp_bullets if b.get('status') in ['sent','replied'] or b.get('sent_date')]
waiting = [b for b in email_bullets+whatsapp_bullets if b.get('status') == 'sent' and not b.get('replied')]
replied = [b for b in email_bullets+whatsapp_bullets if b.get('replied') == True or b.get('status') == 'replied']
alive_email = [b for b in email_bullets if b.get('status') in ['researched','verified','gated'] and not b.get('sent_date')]
alive_wa = [b for b in whatsapp_bullets if b.get('status') in ['researched','verified','gated'] and not b.get('sent_date')]

print()
print('=== SUMMARY ===')
print(f"TOTAL_BULLETS: email={total_email} wa={total_wa} combined={total_email+total_wa}")
print(f"TOTAL_SENT: {len(sent)}")
print(f"WAITING_REPLY: {len(waiting)}")
print(f"REPLIED: {len(replied)}")
print(f"ALIVE_UNSENT: email={len(alive_email)} wa={len(alive_wa)} combined={len(alive_email)+len(alive_wa)}")
print(f"TODAY_NEW_SENT: email={len(today_sent_email)} wa={len(today_sent_wa)} combined={len(today_sent_email)+len(today_sent_wa)}")
