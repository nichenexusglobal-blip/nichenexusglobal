#!/usr/bin/env python3
"""Read full content of 6 supplier emails by searching IMAP"""
import imaplib, email, json, sys, re, traceback
from email.header import decode_header

USER = 'pen@nichenexusglobal.com'
PASS = '4cd7vQ4GV59ATxxt'

targets = [
    ('info@bloopower.com', 'Bloopower'),
    ('coco@califepower.com', 'CALIFE/Coco'),
    ('export9@anern.com', 'Anern/Luke'),
    ('sales06@pecron.com', 'Pecron/Chris'),
]

try:
    mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993, timeout=20)
    mail.login(USER, PASS)
    mail.select('INBOX')
    
    for sender, label in targets:
        print(f"\n{'='*60}")
        print(f"=== {label} ({sender}) ===")
        print('='*60)
        
        status, data = mail.search(None, f'FROM "{sender}"')
        mids = data[0].split() if data[0] else []
        print(f"Messages found: {len(mids)}")
        
        for mid in mids[-5:]:  # Last 5 from each
            status, d = mail.fetch(mid, '(RFC822)')
            if status != 'OK': continue
            if not d or not d[0]: continue
            try:
                msg = email.message_from_bytes(d[0][1])
            except:
                continue
            
            # Subject
            subj_parts = decode_header(msg['Subject'] or '')
            subj = ''
            for part, charset in subj_parts:
                if isinstance(part, bytes):
                    subj += part.decode(charset or 'utf-8', errors='replace')
                else:
                    subj += str(part)
            print(f"\n--- {msg['Date']} ---")
            print(f"Subject: {subj[:150]}")
            
            # Body
            body = ''
            if msg.is_multipart():
                for part in msg.walk():
                    ct = part.get_content_type()
                    if ct == 'text/plain':
                        try:
                            body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                        except:
                            body = ''
                        break
                    elif ct == 'text/html' and not body:
                        try:
                            body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                            body = re.sub(r'<[^>]+>', ' ', body)
                            body = re.sub(r'\s+', ' ', body)
                        except:
                            body = ''
            else:
                try:
                    body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
                except:
                    body = ''
            
            print(f"Body:\n{body[:800].strip()}\n")
    
    mail.logout()
    
except Exception as e:
    sys.stderr.write(f"ERROR: {e}\n{traceback.format_exc()}\n")
    sys.exit(1)
