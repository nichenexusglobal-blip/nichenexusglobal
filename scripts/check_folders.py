#!/usr/bin/env python3
"""List IMAP folders and check them for supplier replies"""
import imaplib, sys, traceback

USER = 'pen@nichenexusglobal.com'
PASS = '4cd7vQ4GV59ATxxt'

try:
    mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993, timeout=20)
    mail.login(USER, PASS)
    
    # List all folders
    status, folders = mail.list()
    print("=== IMAP FOLDERS ===")
    for f in folders:
        if isinstance(f, bytes):
            f = f.decode('utf-8', errors='replace')
        print(f"  {f}")
    
    # Try each folder for supplier replies
    suppliers = {
        'Pecron/Chris': 'sales06@pecron.com',
        'Anern/Luke': 'export9@anern.com', 
        'CALIFE/Coco': 'coco@califepower.com',
    }
    
    # Check INBOX first
    mail.select('INBOX')
    status, data = mail.search(None, 'ALL')
    mids = data[0].split() if data[0] else []
    print(f"\nINBOX: {len(mids)} total")
    
    # Look for the specific subjects we know exist
    # The replies would have "Re:" or "回复：" prefix
    for mid in reversed(mids[-100:]):  # Check last 100
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
        
        # Extract subject line
        subj = ''
        for line in hdr.split('\n'):
            if line.startswith('Subject:'):
                subj = line[8:].strip()
                break
        
        # Check if it's a real supplier reply (not cron, not bounce)
        if any(kw in subj.lower() for kw in ['re:', '回复', 'fwd', 'fw:']):
            if 'hermes' not in subj.lower() and 'cron' not in subj.lower() and 'harness' not in subj.lower() and '退信' not in subj and 'undeliver' not in subj.lower():
                from_hdr = ''
                for line in hdr.split('\n'):
                    if line.startswith('From:'):
                        from_hdr = line[5:].strip()
                        break
                print(f"\n  Reply found!")
                print(f"  From: {from_hdr[:80]}")
                print(f"  Subject: {subj[:100]}")
    
    mail.logout()

except Exception as e:
    sys.stderr.write(f"ERROR: {e}\n{traceback.format_exc()}\n")
    sys.exit(1)
