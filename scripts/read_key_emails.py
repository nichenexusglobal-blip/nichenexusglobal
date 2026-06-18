#!/usr/bin/env python3
"""Read bodies of key emails from today's inbox."""
import imaplib, email, os
from email.header import decode_header
from datetime import datetime, timezone, timedelta
import re
import json

TZ = timezone(timedelta(hours=8))
today = datetime.now(TZ)

def decode_str(s):
    if s is None: return ''
    parts = decode_header(s)
    result = []
    for part, charset in parts:
        if isinstance(part, bytes):
            try: result.append(part.decode(charset or 'utf-8', errors='replace'))
            except: result.append(part.decode('utf-8', errors='replace'))
        else: result.append(str(part))
    return ''.join(result)

def get_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                    break
                except:
                    pass
            elif ct == "text/html" and not body:
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
        except:
            body = str(msg.get_payload())
    return body[:3000]

mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993)
mail.login('pen@nichenexusglobal.com', os.environ.get('NICHE_EMAIL_PASSWORD', ''))
mail.select('INBOX')

s, d = mail.search(None, f'SINCE {today.strftime("%d-%b-%Y")}')
today_ids = d[0].split() if d[0] else []

# Interesting indices (0-based): 
# 6 (Google bounce), 8 (boemargrup bounce), 
# 18 (福建华日), 20 (MECO Power), 21 (Lansinestorage), 22 (Shunxiang), 26 (Lansinestorage 2)
# Also all PostMaster bounces: 4,5,7,10,11,12,13,14,15,25
interesting = [6, 8, 18, 20, 21, 22, 26]
bounce_indices = [4, 5, 7, 10, 11, 12, 13, 14, 15, 25]

results = {"supplier_replies": [], "bounces": [], "postmaster_bounces": []}

for idx in interesting + bounce_indices:
    if idx >= len(today_ids):
        continue
    mid = today_ids[idx]
    s, data = mail.fetch(mid, '(RFC822)')
    if s != 'OK':
        continue
    
    msg = email.message_from_bytes(data[0][1])
    subject = decode_str(msg['Subject'])
    from_ = decode_str(msg['From'])
    body = get_body(msg)
    
    entry = {"from": from_[:80], "subject": subject[:120], "body_preview": body[:2000]}
    
    if idx in interesting:
        results["supplier_replies"].append(entry)
    else:
        results["postmaster_bounces"].append(entry)

for r in results["supplier_replies"]:
    print(f"\n{'='*60}")
    print(f"FROM: {r['from']}")
    print(f"SUBJ: {r['subject']}")
    print(f"{'='*60}")
    print(r['body_preview'][:2000])

for r in results["postmaster_bounces"]:
    print(f"\n{'='*60}")
    print(f"BOUNCE FROM: {r['from']}")
    print(f"SUBJ: {r['subject']}")
    print(f"{'='*60}")
    print(r['body_preview'][:1500])

# Also check the Google bounce
print(f"\n{'='*60}")
print(f"GOOGLE BOUNCE #{len(results['supplier_replies'])+1}")
r = results["supplier_replies"][0] if results["supplier_replies"] else None
if r and 'google' in r['from'].lower():
    print(r['body_preview'][:2000])

mail.close()
mail.logout()

# Save to file
with open('/tmp/inbox_bodies.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print("\n✅ Saved to /tmp/inbox_bodies.json")
