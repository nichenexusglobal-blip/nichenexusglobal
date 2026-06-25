#!/usr/bin/env python3
"""Extract original recipient emails from bounces"""
import imaplib
import email
import sys
import re

def safe_str(s):
    if s is None:
        return ''
    return str(s)

def decode_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype in ("text/plain", "text/html"):
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    try:
                        body += payload.decode(charset, errors='replace')
                    except:
                        body += payload.decode('utf-8', errors='replace')
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or 'utf-8'
            try:
                body = payload.decode(charset, errors='replace')
            except:
                body = payload.decode('utf-8', errors='replace')
    return body

def extract_recipients(body):
    """Extract original recipient from bounce body"""
    emails = set()
    # Common patterns
    for pat in [r'<([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})>',
                r'Original-Recipient:\s*[^;]*;\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'Final-Recipient:\s*[^;]*;\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})']:
        found = re.findall(pat, body, re.IGNORECASE)
        for f in found:
            if 'nichenexusglobal.com' not in f and 'pen@' not in f:
                emails.add(f.lower())
    return emails

def main():
    try:
        mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993)
        mail.login('pen@nichenexusglobal.com', '4cd7vQ4GV59ATxxt')
        mail.select('INBOX')
        
        status, ids = mail.search(None, 'ALL')
        ids = ids[0].split()
        recent = ids[-200:] if len(ids) > 200 else ids
        
        all_bounced = set()
        
        for mid in reversed(recent):
            status, data = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
            if status != 'OK':
                continue
            msg = email.message_from_bytes(data[0][1])
            frm = safe_str(msg.get('From'))
            subj = safe_str(msg.get('Subject'))
            
            is_bounce = any(k in frm.lower() for k in ['postmaster', 'mailer-daemon'])
            if not is_bounce:
                is_bounce = any(k in subj for k in ['Undelivered', 'Mail delivery failed', 'Delivery Status'])
            
            if is_bounce:
                # Get full body
                status2, data2 = mail.fetch(mid, '(RFC822)')
                if status2 != 'OK':
                    continue
                full = email.message_from_bytes(data2[0][1])
                body = decode_email_body(full)
                recipients = extract_recipients(body)
                all_bounced.update(recipients)
        
        print(f'Unique bounced recipients found: {len(all_bounced)}')
        for r in sorted(all_bounced):
            print(f'  {r}')
        
        mail.logout()
        return 0
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
