#!/usr/bin/env python3
"""Daily review: Check inbox via IMAP"""
import imaplib
import email
from email.header import decode_header
import time
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
today_start = datetime.now(TZ).strftime("%d-%b-%Y")

try:
    mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993, timeout=30)
    mail.login('pen@nichenexusglobal.com', '4cd7v4QGV59ATxxt')
    print("LOGIN_OK")
    
    # Select INBOX
    status, data = mail.select('INBOX')
    print(f"INBOX selected: {status}")
    
    # Search for today's messages
    status, ids = mail.search(None, f'(SINCE {today_start})')
    all_ids = ids[0].split() if ids[0] else []
    print(f"Today's total messages: {len(all_ids)}")
    
    if all_ids:
        # Fetch batch of headers
        for i in range(0, len(all_ids), 50):
            batch = all_ids[i:i+50]
            batch_str = ','.join([id.decode() if isinstance(id, bytes) else str(id) for id in batch])
            status, msgs = mail.fetch(batch_str, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
            if status != 'OK':
                continue
            for msg_data in msgs:
                if isinstance(msg_data, tuple) and len(msg_data) > 1:
                    header_data = msg_data[1]
                    msg = email.message_from_bytes(header_data)
                    from_addr = msg.get('From', '')
                    subject = msg.get('Subject', '')
                    date_str = msg.get('Date', '')
                    
                    # Decode subject
                    decoded_parts = decode_header(subject)
                    subject_decoded = ''
                    for part, charset in decoded_parts:
                        if isinstance(part, bytes):
                            try:
                                subject_decoded += part.decode(charset or 'utf-8', errors='replace')
                            except:
                                subject_decoded += part.decode('utf-8', errors='replace')
                        else:
                            subject_decoded += part
                    
                    # Skip system emails
                    from_lower = from_addr.lower() if from_addr else ''
                    if ('pen@nichenexusglobal.com' in from_lower or 
                        'hermes agent' in subject_decoded.lower() or
                        'cron' in subject_decoded.lower() or
                        'gateway' in subject_decoded.lower()):
                        continue
                    
                    print(f"REAL_EMAIL|From: {from_addr}|Subject: {subject_decoded}|Date: {date_str}")
    
    mail.logout()
    
except imaplib.IMAP4.error as e:
    print(f"IMAP_ERROR: {e}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
