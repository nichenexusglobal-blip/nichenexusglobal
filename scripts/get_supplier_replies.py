#!/usr/bin/env python3
"""Get specific supplier reply emails"""
import imaplib, email, sys, traceback
from email.header import decode_header

USER = 'pen@nichenexusglobal.com'
PASS = '4cd7vQ4GV59ATxxt'

suppliers = {
    'Pecron': 'sales06@pecron.com',
    'Anern': 'export9@anern.com',
    'CALIFE': 'coco@califepower.com',
    'Bloopower': 'info@bloopower.com',
}

try:
    mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993, timeout=20)
    mail.login(USER, PASS)
    mail.select('INBOX')

    for label, sender in suppliers.items():
        print(f"\n{'='*60}")
        print(f"=== {label} ({sender}) ===")
        print('='*60)
        
        status, data = mail.search(None, f'FROM "{sender}"')
        mids = data[0].split() if data[0] else []
        
        real_emails = 0
        for mid in mids:
            status, d = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
            if status != 'OK': continue
            if not d or not d[0]: continue
            try:
                raw = d[0][1]
                if isinstance(raw, bytes):
                    hdr = raw.decode('utf-8', errors='replace')
                else:
                    continue
            except:
                continue
            
            # Skip cron/Hermes responses
            if 'Hermes Agent' in hdr or 'Cronjob' in hdr or 'Harness' in hdr:
                continue
            
            # Extract subject
            subj = ''
            for line in hdr.split('\n'):
                if line.startswith('Subject:'):
                    subj = line[8:].strip()
                    break
            
            # Decode subject if encoded
            if '=?' in subj:
                try:
                    subj_parts = decode_header(subj)
                    subj = ''
                    for part, charset in subj_parts:
                        if isinstance(part, bytes):
                            subj += part.decode(charset or 'utf-8', errors='replace')
                        else:
                            subj += str(part)
                except:
                    pass
            
            real_emails += 1
            print(f"\n  [{real_emails}] Subject: {subj[:120]}")
            
            # Get full body
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
            
            # Extract date
            date_str = str(msg['Date'] or '?')
            
            # Print body without quoted text (stop at first ">" or "-----Original Message-----")
            lines = body.split('\n')
            useful = []
            for line in lines:
                if line.strip().startswith('>') or 'Original Message' in line or 'From:' in line and 'Sent:' in line:
                    break
                useful.append(line)
            
            body_clean = '\n'.join(useful).strip()
            if body_clean:
                print(f"  Date: {date_str}")
                print(f"  Body:\n{body_clean[:800]}\n")
        
        if real_emails == 0:
            print("  (no real supplier emails found - all were cron/Hermes responses)")
    
    mail.logout()

except Exception as e:
    sys.stderr.write(f"ERROR: {e}\n{traceback.format_exc()}\n")
    sys.exit(1)
