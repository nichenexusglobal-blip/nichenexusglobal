#!/usr/bin/env python3
"""Daily review: Check Sent Messages via IMAP"""
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
today = datetime.now(TZ).strftime("%d-%b-%Y")

try:
    mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993, timeout=30)
    mail.login('pen@nichenexusglobal.com', '4cd7v4QGV59ATxxt')
    print("LOGIN_OK")
    
    # Try selecting Sent Messages with quotes
    status, data = mail.select('"Sent Messages"')
    print(f"Sent Messages selected: {status}")
    
    if status != 'OK':
        # Try alternative names
        for folder in ['"已发送"', '"Sent"', '"Sent Items"', '"发件箱"']:
            status, data = mail.select(folder)
            print(f"Trying {folder}: {status}")
            if status == 'OK':
                break
    
    if status == 'OK':
        # Search for today's sent emails
        status, ids = mail.search(None, f'(SINCE {today})')
        all_ids = ids[0].split() if ids[0] else []
        print(f"Today's sent count: {len(all_ids)}")
        
        real_emails = []
        if all_ids:
            for i in range(0, len(all_ids), 50):
                batch = all_ids[i:i+50]
                batch_str = ','.join([id.decode() if isinstance(id, bytes) else str(id) for id in batch])
                status, msgs = mail.fetch(batch_str, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT TO DATE)])')
                if status != 'OK':
                    continue
                for msg_data in msgs:
                    if isinstance(msg_data, tuple) and len(msg_data) > 1:
                        header_data = msg_data[1]
                        msg = email.message_from_bytes(header_data)
                        to_addr = msg.get('To', '')
                        subject = msg.get('Subject', '')
                        date_str = msg.get('Date', '')
                        
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
                        
                        print(f"SENT|To: {to_addr}|Subject: {subject_decoded}|Date: {date_str}")
    
    mail.logout()
    
except imaplib.IMAP4.error as e:
    print(f"IMAP_ERROR: {e}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
