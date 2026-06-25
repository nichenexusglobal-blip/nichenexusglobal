#!/usr/bin/env python3
"""Check for bounce emails from today specifically (June 19)"""
import imaplib
import email
import sys

def safe_str(s):
    if s is None:
        return ''
    return str(s)

def main():
    try:
        mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993)
        mail.login('pen@nichenexusglobal.com', '4cd7vQ4GV59ATxxt')
        mail.select('INBOX')
        
        status, ids = mail.search(None, 'ALL')
        ids = ids[0].split()
        recent = ids[-100:]
        bounce_today = 0
        
        for mid in reversed(recent):
            status, data = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
            if status != 'OK':
                continue
            msg = email.message_from_bytes(data[0][1])
            frm = safe_str(msg.get('From'))
            subj = safe_str(msg.get('Subject'))
            dt = safe_str(msg.get('Date'))
            
            # Check for bounces
            is_bounce = False
            for kw in ['postmaster', 'mailer-daemon', 'Mail Delivery']:
                if kw in frm.lower() or kw in subj:
                    is_bounce = True
                    break
                    
            if is_bounce and '19 Jun 2026' in dt:
                bounce_today += 1
                print(f'Today bounce: {frm[:40]} | {subj[:60]} | {dt}')
        
        if bounce_today == 0:
            print('No bounce emails from today (June 19) found')
        
        mail.logout()
        return 0
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
