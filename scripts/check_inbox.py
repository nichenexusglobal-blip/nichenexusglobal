#!/usr/bin/env python3
"""检查收件箱 — IMAP imap.exmail.qq.com"""
import imaplib
import email
from email.header import decode_header
import datetime

IMAP_SERVER = "imap.exmail.qq.com"
IMAP_PORT = 993
USER = "pen@nichenexusglobal.com"
PASSWORD = "4cd7v4QGV59ATxxt"

today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
today_str = today.strftime("%d-%b-%Y")

try:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(USER, PASSWORD)
    print("IMAP LOGIN OK")
    
    # List all folders
    status, folders = mail.list()
    print(f"\nFolders: {len(folders)} found")
    for f in folders[:20]:
        print(f"  {f}")
    
    # Check INBOX
    status, data = mail.select("INBOX")
    print(f"\nINBOX select: {status}")
    print(f"Total messages: {data[0].decode() if data else 'unknown'}")
    
    # Search for today's messages
    status, msg_ids = mail.search(None, f'(SINCE {today_str})')
    if status != 'OK':
        print(f"Search failed: {status}")
    else:
        ids = msg_ids[0].split() if msg_ids[0] else []
        print(f"\nMessages since {today_str}: {len(ids)}")
        
        real_emails = []
        for mid in ids:
            status, data = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
            if status != 'OK':
                continue
            header_data = data[0][1] if len(data[0]) > 1 else b''
            msg = email.message_from_bytes(header_data)
            fr = msg.get('From', '')
            subj = msg.get('Subject', '')
            date = msg.get('Date', '')
            
            # Filter out system emails
            skip_keywords = ['hermes', 'cronjob', 'gateway', 'postmaster', 'mailer-daemon',
                           'noreply', 'no-reply', 'bounce', 'undeliverable']
            is_system = any(kw in (fr + subj).lower() for kw in skip_keywords)
            
            print(f"  [{mid.decode()}]: From={fr} | Subject={subj[:60]} | {date}")
            
            if not is_system and 'pen@nichenexusglobal.com' not in fr.lower():
                real_emails.append((mid, fr, subj, date))
        
        print(f"\n=== REAL EMAILS (non-system) today: {len(real_emails)} ===")
        for mid, fr, subj, date in real_emails:
            # Fetch full body
            status, data = mail.fetch(mid, '(BODY.PEEK[TEXT])')
            if status == 'OK':
                body = data[0][1].decode('utf-8', errors='replace')[:500] if len(data[0]) > 1 else ''
            else:
                body = '(could not fetch body)'
            print(f"\n--- From: {fr}")
            print(f"Subject: {subj}")
            print(f"Date: {date}")
            print(f"Body preview: {body[:300]}")
            print("---")
    
    mail.logout()
    
except imaplib.IMAP4.error as e:
    print(f"IMAP ERROR: {e}")
except Exception as e:
    print(f"ERROR: {e}")
