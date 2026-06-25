#!/usr/bin/env python3
"""Fast check: get most recent supplier replies from INBOX"""
import imaplib, email, sys
from email.header import decode_header

USER = 'pen@nichenexusglobal.com'
PASS = '4cd7vQ4GV59ATxxt'

# These are the specific real supplier emails we know exist
# Search by specific subject-only patterns that aren't cron/bounce
search_domains = ['@pecron.com', '@anern.com', '@califepower.com', '@bloopower.com',
                  '@meco-', '@shunxiang', '@ie-energy', '@powerlfp']

try:
    mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993, timeout=20)
    mail.login(USER, PASS)
    mail.select('INBOX')
    
    # Search for ALL messages that are replies (not our sent ones)
    status, data = mail.search(None, 'ALL')
    mids = data[0].split() if data[0] else []
    
    found = 0
    for mid in reversed(mids[-394:]):  # All messages
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
        
        # Skip known system messages fast
        if 'Hermes Agent' in hdr or 'Harness' in hdr or 'nichenexusglobal.com的退信' in hdr:
            continue
        if 'Undeliverable' in hdr or 'Mail Delivery' in hdr or 'Delivery Status' in hdr:
            continue
        
        # Extract subject
        subj = ''
        for line in hdr.split('\n'):
            if line.startswith('Subject:'):
                subj = line[8:].strip()
                break
        
        # Try to decode
        if '=?' in subj:
            try:
                sp = decode_header(subj)
                subj = ''
                for p, c in sp:
                    if isinstance(p, bytes):
                        subj += p.decode(c or 'utf-8', errors='replace')
                    else:
                        subj += str(p)
            except:
                pass
        
        # Extract From
        from_ = ''
        for line in hdr.split('\n'):
            if line.startswith('From:'):
                from_ = line[5:].strip()
                break
        
        # Is this a real reply thread? Check for Re:/回复 prefix
        is_reply = subj.lower().startswith('re:') or subj.startswith('回复')
        
        if is_reply or any(dom in from_.lower() for dom in search_domains):
            found += 1
            print(f"\n--- #{found} ---")
            print(f"From: {from_[:80]}")
            print(f"Subject: {subj[:120]}")
            
            # Quick date
            for line in hdr.split('\n'):
                if line.startswith('Date:'):
                    print(f"Date: {line[5:].strip()[:40]}")
                    break
    
    print(f"\n\nTotal real replies found: {found}")
    mail.logout()

except Exception as e:
    sys.stderr.write(f"ERROR: {e}\n")
    sys.exit(1)
