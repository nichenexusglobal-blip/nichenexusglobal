#!/usr/bin/env python3
"""Check today's inbox for non-system emails (filtering out Hermes cron noise)."""
import imaplib
import ssl
import email
from email.header import decode_header

def decode_str(s):
    parts = decode_header(s)
    result = []
    for part, charset in parts:
        if isinstance(part, bytes):
            try:
                result.append(part.decode(charset or 'utf-8', errors='replace'))
            except:
                result.append(part.decode('utf-8', errors='replace'))
        else:
            result.append(part)
    return ''.join(result)

SYSTEM_DOMAINS = ['pen@nichenexusglobal.com']
SYSTEM_KEYWORDS = ['Hermes', 'Cronjob', 'Gateway', 'cron']

ctx = ssl.create_default_context()
mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993, ssl_context=ctx)
try:
    mail.login('pen@nichenexusglobal.com', '4cd7vQ4GV59ATxxt')
except Exception as e:
    print(f"IMAP_LOGIN_FAIL: {e}")
    exit(1)

mail.select('INBOX')
typ, data = mail.search(None, 'ALL')
ids = data[0].split()
print(f"Total messages: {len(ids)}")

# Check last 50 messages
recent = ids[-50:]
real_count = 0
for i in recent:
    typ, msg_data = mail.fetch(i, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
    raw = msg_data[0][1].decode('utf-8', errors='replace')
    
    from_hdr = ''
    subj_hdr = ''
    date_hdr = ''
    for line in raw.split('\r\n'):
        if line.upper().startswith('FROM:'):
            from_hdr = line[5:].strip()
        elif line.upper().startswith('SUBJECT:'):
            subj_hdr = line[8:].strip()
        elif line.upper().startswith('DATE:'):
            date_hdr = line[5:].strip()
    
    # Filter system emails
    is_system = False
    for dom in SYSTEM_DOMAINS:
        if dom in from_hdr:
            is_system = True
            break
    for kw in SYSTEM_KEYWORDS:
        if kw.lower() in subj_hdr.lower():
            is_system = True
            break
    
    if is_system:
        continue
    
    real_count += 1
    print(f"\n--- Real Email #{real_count} ---")
    print(f"From: {from_hdr}")
    print(f"Subject: {subj_hdr}")
    print(f"Date: {date_hdr}")

print(f"\n\nReal non-system emails in last 50: {real_count}")

mail.logout()
