#!/usr/bin/env python3
"""Search for specific supplier email threads by subject keywords"""
import imaplib, email, sys, re, traceback
from email.header import decode_header

USER = 'pen@nichenexusglobal.com'
PASS = '4cd7vQ4GV59ATxxt'

# Known supplier subjects from initial scan
SEARCH_TERMS = [
    ('Bloopower', 'info@bloopower.com', ['RFQ', '300W', '1000W', '3600W']),
    ('CALIFE/Coco', 'coco@califepower.com', ['RFQ', '1000W', '2000W', 'OEM']),
    ('Anern/Luke', 'export9@anern.com', ['Inquiry', 'Portable power']),
    ('Pecron/Chris', 'sales06@pecron.com', ['FOB quote', 'shipping', 'Nigeria delivery']),
]

try:
    mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993, timeout=20)
    mail.login(USER, PASS)
    mail.select('INBOX')
    
    for label, sender, keywords in SEARCH_TERMS:
        print(f"\n{'='*60}")
        print(f"=== {label} ({sender}) ===")
        print('='*60)
        
        # Search by sender
        status, data = mail.search(None, f'FROM "{sender}"')
        mids = data[0].split() if data[0] else []
        print(f"Total from {sender}: {len(mids)}")
        
        for mid in mids:
            status, d = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
            if status != 'OK': continue
            if not d or not d[0]: continue
            try:
                raw = d[0][1]
                if isinstance(raw, bytes):
                    msg_str = raw.decode('utf-8', errors='replace')
                else:
                    continue
            except:
                continue
            
            # Skip cron/replay responses
            if 'Hermes Agent' in msg_str or 'Cronjob' in msg_str or 'Harness' in msg_str:
                continue
            
            # Extract subject
            subj_match = re.search(r'^Subject: (.+)$', msg_str, re.MULTILINE)
            if not subj_match:
                continue
            subj = subj_match.group(1).strip()
            
            # Extract date
            date_match = re.search(r'^Date: (.+)$', msg_str, re.MULTILINE)
            date_str = date_match.group(1).strip() if date_match else '?'
            
            print(f"\n  [{date_str}]")
            print(f"  Subject: {subj[:150]}")
            
            # Now get the full body
            status2, d2 = mail.fetch(mid, '(RFC822)')
            if status2 != 'OK': continue
            if not d2 or not d2[0]: continue
            try:
                msg = email.message_from_bytes(d2[0][1])
            except:
                continue
            
            body = ''
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        try:
                            body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                        except:
                            body = ''
                        break
            else:
                try:
                    body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
                except:
                    body = ''
            
            # Show body (skip quoted text)
            body_clean = body[:1000].strip()
            print(f"  Body:\n{body_clean}\n")
    
    mail.logout()
    
except Exception as e:
    sys.stderr.write(f"ERROR: {e}\n{traceback.format_exc()}\n")
    sys.exit(1)
