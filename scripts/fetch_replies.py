#!/usr/bin/env python3
"""Fetch full content of 4 specific supplier emails"""
import imaplib, email, sys, re

USER = 'pen@nichenexusglobal.com'
PASS = '4cd7vQ4GV59ATxxt'

try:
    mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993, timeout=30)
    mail.login(USER, PASS)
    mail.select('INBOX')
    
    # Search by each supplier email individually
    searches = [
        ('Pecron/Chris #1', 'FROM "sales06@pecron.com" SUBJECT "Nigeria"'),
        ('Pecron/Chris #2', 'FROM "sales06@pecron.com" SUBJECT "shipping cost"'),
        ('Anern/Luke #1', 'FROM "export9@anern.com" SUBJECT "Inquiry"'),
        ('Anern/Luke #2', 'FROM "export9@anern.com" SUBJECT "Inquiry"'),
    ]
    
    for label, search_str in searches:
        print(f"\n{'='*60}")
        print(f"=== {label} ===")
        print('='*60)
        
        status, data = mail.search(None, search_str)
        mids = data[0].split() if data[0] else []
        if not mids:
            print("  No results")
            continue
        
        # Get the LAST result (most recent) for each search
        mid = mids[-1]
        status, d = mail.fetch(mid, '(RFC822)')
        if status != 'OK' or not d or not d[0]:
            print("  Fetch failed")
            continue
        
        try:
            msg = email.message_from_bytes(d[0][1])
        except:
            print("  Parse failed")
            continue
        
        # Get subject
        subj_parts = msg.get('Subject', '')
        if isinstance(subj_parts, str) and '=?' in subj_parts:
            from email.header import decode_header
            sp = decode_header(subj_parts)
            subj = ''
            for p, c in sp:
                if isinstance(p, bytes):
                    subj += p.decode(c or 'utf-8', errors='replace')
                else:
                    subj += str(p)
        else:
            subj = str(subj_parts)
        
        # Get body
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
        
        print(f"Subject: {subj[:150]}")
        print(f"Date: {msg['Date']}")
        
        # Clean body - remove quoted text
        lines = body.split('\n')
        clean = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('>') or 'Original Message' in stripped or '---Original---' in stripped:
                break
            if stripped.startswith('From:') or stripped.startswith('Sent:') or stripped.startswith('Date:'):
                continue
            clean.append(line)
        
        body_clean = '\n'.join(clean).strip()
        if body_clean:
            print(f"\nBody:\n{body_clean[:1500]}\n")
        else:
            print("  (empty body after cleaning)")
    
    mail.logout()

except Exception as e:
    sys.stderr.write(f"ERROR: {e}\n")
    sys.exit(1)
