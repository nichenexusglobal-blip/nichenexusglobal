#!/usr/bin/env python3
"""Check full email bodies for today's (June 24) important emails."""
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

def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == 'text/plain':
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode('utf-8', errors='replace')[:2000]
            elif ct == 'text/html' and not msg.is_multipart():
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode('utf-8', errors='replace')[:2000]
        return "[No text/plain part found]"
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            return payload.decode('utf-8', errors='replace')[:2000]
        return "[Empty body]"

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
total = len(ids)
print(f"Total messages: {total}")

# Check last 50 for June 24 emails
recent = ids[-50:]
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
    
    # Only get June 24 non-system emails
    if '24 Jun 2026' in date_hdr or '24 Jun 2026' in date_hdr:
        is_system = ('pen@nichenexusglobal.com' in from_hdr) or any(k.lower() in subj_hdr.lower() for k in ['Hermes', 'Cronjob', 'Gateway', 'cron'])
        if is_system:
            continue
        print(f"\n=== TODAY'S EMAIL ===")
        print(f"From: {from_hdr}")
        print(f"Subject: {subj_hdr}")
        print(f"Date: {date_hdr}")
        # Fetch full body
        typ2, body_data = mail.fetch(i, '(BODY.PEEK[])')
        msg = email.message_from_bytes(body_data[0][1])
        body = get_body(msg)
        print(f"Body:\n{body[:1500]}")
        print("===")

# Also specifically check the PostMaster email and Bella email
# Let me search by looking at ALL messages for today
print("\n\n=== SEARCHING ALL FOR JUNE 24 REAL EMAILS ===")
for i in ids[-100:]:
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
    
    # Check if it's today (Jun 24)
    if '24 Jun 2026' in date_hdr or 'Wed, 24 Jun 2026' in date_hdr:
        is_system = ('pen@nichenexusglobal.com' in from_hdr)
        if is_system:
            continue
        print(f"\nFrom: {from_hdr}")
        print(f"Subject: {subj_hdr}")
        print(f"Date: {date_hdr}")
        typ2, body_data = mail.fetch(i, '(BODY.PEEK[])')
        msg = email.message_from_bytes(body_data[0][1])
        body = get_body(msg)
        print(f"Body:\n{body[:1200]}")

mail.logout()
