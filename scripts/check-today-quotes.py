#!/usr/bin/env python3
"""Fetch full body of today's sent emails to check if they contain pricing"""
import imaplib
import email
import sys
from email.header import decode_header

def safe_str(s):
    if s is None:
        return ''
    return str(s)

def decode_email_body(msg):
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
        
        status, data = mail.select('"Sent Messages"')
        if status != 'OK':
            print('Failed to select')
            return 1
        
        status, ids = mail.search(None, 'ALL')
        ids = ids[0].split()
        recent_ids = ids[-200:] if len(ids) > 200 else ids
        
        for mid in reversed(recent_ids):
            status, data = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE TO)])')
            if status != 'OK':
                continue
            msg = email.message_from_bytes(data[0][1])
            dt = safe_str(msg.get('Date'))
            subj = safe_str(msg.get('Subject'))
            to = safe_str(msg.get('To'))
            
            if '19 Jun 2026' not in dt:
                continue
            if 'Hermes Agent' in subj:
                continue
            
            # Fetch full body
            status2, data2 = mail.fetch(mid, '(RFC822)')
            if status2 != 'OK':
                continue
            full_msg = email.message_from_bytes(data2[0][1])
            body = decode_email_body(full_msg)
            
            # Check for pricing in body
            has_pricing = any(k in body.lower() for k in ['$', 'usd', 'fob', 'price', 'pricing', '报价'])
            print(f'To: {to[:40]}')
            print(f'Subj: {subj[:60]}')
            print(f'Has pricing: {has_pricing}')
            print(f'Body (first 300): {body[:300]}')
            print('---')
        
        mail.logout()
        return 0
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
