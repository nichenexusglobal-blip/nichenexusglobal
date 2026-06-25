#!/usr/bin/env python3
"""Check today's inbox - scan all messages, find real (non-system) ones and bounces"""
import imaplib
import email
import sys

def safe_str(s):
    """Safely convert any email header to string"""
    if s is None:
        return ''
    # In Python 3.11, Header.__str__() works correctly
    return str(s)

def main():
    try:
        mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993)
        mail.login('pen@nichenexusglobal.com', '4cd7vQ4GV59ATxxt')
        mail.select('INBOX')
        
        status, ids = mail.search(None, 'ALL')
        ids = ids[0].split()
        total = len(ids)
        print(f'INBOX total: {total} messages')
        
        # Scan all messages - fetch in batches of 100
        batch_size = 100
        all_real = []
        all_bounces = []
        
        for start in range(max(0, total - 500), total, batch_size):
            batch = ids[start:start+batch_size]
            for mid in batch:
                status, data = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
                if status != 'OK':
                    continue
                msg = email.message_from_bytes(data[0][1])
                frm = safe_str(msg.get('From'))
                subj = safe_str(msg.get('Subject'))
                dt = safe_str(msg.get('Date'))
                
                # Skip system/internal emails
                if 'pen@nichenexusglobal.com' in frm:
                    if any(k in subj for k in ['Hermes', 'Cron', 'Gateway']):
                        continue
                if any(k in subj for k in ['Hermes Agent', 'Cronjob']):
                    continue
                if frm == '' and subj == '':
                    continue
                    
                # Check if bounce
                is_bounce = False
                for keyword in ['postmaster', 'mailer-daemon', 'mail delivery system', 'mail delivery failed']:
                    if keyword in frm.lower():
                        is_bounce = True
                        break
                if not is_bounce:
                    for keyword in ['Undelivered', 'Returned mail', 'Mail delivery failed', 'Delivery Status Notification', 'Mail Delivery System']:
                        if keyword in subj:
                            is_bounce = True
                            break
                
                entry = (frm, subj, dt)
                if is_bounce:
                    all_bounces.append(entry)
                else:
                    all_real.append(entry)
        
        print(f'\n=== REAL EMAILS (non-system, max 30 shown) ===')
        print(f'Count: {len(all_real)}')
        for frm, subj, dt in reversed(all_real[-30:]):
            print(f'  From: {frm[:50]} | Subj: {subj[:80]} | Date: {dt}')
        
        print(f'\n=== BOUNCE/UNDELIVERED (max 20 shown) ===')
        print(f'Count: {len(all_bounces)}')
        for frm, subj, dt in reversed(all_bounces[-20:]):
            print(f'  From: {frm[:50]} | Subj: {subj[:80]} | Date: {dt}')
        
        print(f'\n--- Summary ---')
        print(f'Total INBOX: {total}')
        print(f'Non-system real msgs: {len(all_real)}')
        print(f'Bounces: {len(all_bounces)}')
        
        mail.logout()
        return 0
    except Exception as e:
        print(f'IMAP ERROR: {e}', file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
