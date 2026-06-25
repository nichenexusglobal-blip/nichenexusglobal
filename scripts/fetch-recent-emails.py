#!/usr/bin/env python3
"""Fetch full content of emails for specific senders"""
import imaplib
import email
import sys
from email.header import decode_header

def safe_str(s):
    if s is None:
        return ''
    return str(s)

def decode_email_body(msg):
    """Decode email body from email.message.Message"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    try:
                        body += payload.decode(charset, errors='replace')
                    except:
                        body += payload.decode('utf-8', errors='replace')
                break
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or 'utf-8'
            try:
                body = payload.decode(charset, errors='replace')
            except:
                body = payload.decode('utf-8', errors='replace')
    return body

def main():
    try:
        mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993)
        mail.login('pen@nichenexusglobal.com', '4cd7vQ4GV59ATxxt')
        mail.select('INBOX')
        
        status, ids = mail.search(None, 'ALL')
        ids = ids[0].split()
        total = len(ids)
        
        # Check last 200 messages for real people from last 3 days
        recent_ids = ids[-200:] if total > 200 else ids
        
        for mid in reversed(recent_ids):
            status, data = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
            if status != 'OK':
                continue
            msg = email.message_from_bytes(data[0][1])
            frm = safe_str(msg.get('From'))
            subj = safe_str(msg.get('Subject'))
            dt = safe_str(msg.get('Date'))
            
            # Skip system/internal
            if 'pen@nichenexusglobal.com' in frm and ('Hermes' in subj or 'Cron' in subj):
                continue
            if 'Hermes Agent' in subj:
                continue
            if 'postmaster' in frm.lower() or 'mailer-daemon' in frm.lower():
                continue
            if 'GitGuardian' in frm:
                continue
                
            # Focus on supplier/client replies from June 19
            if '19 Jun 2026' in dt or '18 Jun 2026' in dt:
                # Fetch full body
                status, data2 = mail.fetch(mid, '(RFC822)')
                if status != 'OK':
                    continue
                full_msg = email.message_from_bytes(data2[0][1])
                body = decode_email_body(full_msg)
                print(f'=== {frm[:40]} | {dt} ===')
                print(f'Subject: {subj[:80]}')
                print(f'Body (first 500 chars): {body[:500]}')
                print()
        
        mail.logout()
        return 0
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
