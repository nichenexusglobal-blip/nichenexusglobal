#!/usr/bin/env python3
"""Check June 20 inbox and sent messages"""
import imaplib, email, sys

def main():
    try:
        mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993)
        mail.login('pen@nichenexusglobal.com', '4cd7vQ4GV59ATxxt')
        
        # Check INBOX for June 20
        mail.select('INBOX')
        s, ids = mail.search(None, 'ALL')
        all_ids = ids[0].split()
        total = len(all_ids)
        print(f'INBOX total: {total}')
        
        real_count = 0
        bounce_count = 0
        print('\n=== INBOX - Real non-system emails on June 20 ===')
        for mid in reversed(all_ids[-500:]):
            s, d = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
            if s != 'OK': continue
            msg = email.message_from_bytes(d[0][1])
            dt = str(msg.get('Date', ''))
            frm = str(msg.get('From', ''))
            subj = str(msg.get('Subject', ''))
            
            if '20 Jun 2026' not in dt:
                continue
            
            # Skip system
            if 'pen@nichenexusglobal.com' in frm:
                if any(k in subj for k in ['Hermes','Cron','Gateway','Backup']):
                    continue
            
            # Check bounce
            is_bounce = any(k in frm.lower() for k in ['postmaster','mailer-daemon','mail delivery'])
            if not is_bounce:
                is_bounce = any(k in subj for k in ['Undelivered','Returned mail','Mail delivery failed','Delivery Status'])
            
            if is_bounce:
                bounce_count += 1
                print(f'  [BOUNCE] From:{frm[:50]} | Subj:{subj[:60]} | {dt}')
            else:
                real_count += 1
                print(f'  From:{frm[:50]} | Subj:{subj[:60]} | {dt}')
        
        print(f'\nINBOX Jun20: {real_count} real emails, {bounce_count} bounces')
        
        # Check SENT for June 20
        mail.select('"Sent Messages"')
        s, ids = mail.search(None, 'ALL')
        all_ids = ids[0].split()
        total_sent = len(all_ids)
        print(f'\nSent total: {total_sent}')
        
        sent_count = 0
        supplier_count = 0
        customer_count = 0
        print('=== SENT - Messages on June 20 ===')
        for mid in reversed(all_ids[-300:]):
            s, d = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE TO)])')
            if s != 'OK': continue
            msg = email.message_from_bytes(d[0][1])
            dt = str(msg.get('Date', ''))
            to = str(msg.get('To', '')).strip()
            subj = str(msg.get('Subject', '')).strip()
            
            if '20 Jun 2026' not in dt:
                continue
            
            sent_count += 1
            lower_subj = subj.lower()
            if any(k in lower_subj for k in ['rfq','inquiry','pricing','fob','quote']):
                supp = 'SUPPLIER'
                supplier_count += 1
            else:
                supp = 'CUSTOMER'
                customer_count += 1
            print(f'  [{supp}] To:{to[:50]} | Subj:{subj[:60]} | {dt}')
        
        print(f'\nSENT Jun20: {sent_count} total ({supplier_count} supplier, {customer_count} customer)')
        
        mail.logout()
        return 0
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
