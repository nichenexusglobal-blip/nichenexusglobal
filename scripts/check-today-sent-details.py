#!/usr/bin/env python3
"""Get full details on today's sent messages"""
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
        
        # Use Sent Messages
        status, data = mail.select('"Sent Messages"')
        if status != 'OK':
            print('Failed to select Sent Messages')
            return 1
        
        status, ids = mail.search(None, 'ALL')
        ids = ids[0].split()
        total = len(ids)
        
        recent_ids = ids[-200:] if total > 200 else ids
        today_supplier = 0
        today_customer = 0
        
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
                
            # Categorize
            lower_subj = subj.lower()
            lower_to = to.lower()
            
            has_rfq_keywords = any(k in lower_subj for k in ['rfq', 'inquiry', 'fob', 'pricing', 'quote'])
            is_supplier = has_rfq_keywords or any(k in lower_to for k in ['@alibaba.com'])
            
            if is_supplier:
                today_supplier += 1
                category = 'SUPPLIER RFQ'
            else:
                today_customer += 1
                category = 'CUSTOMER'
            
            print(f'[{category}] To: {to[:50]}')
            print(f'  Subj: {subj[:80]}')
            print(f'  Date: {dt}')
            print()
        
        print(f'--- Today Summary ---')
        print(f'Supplier RFQs: {today_supplier}')
        print(f'Customer outreach: {today_customer}')
        print(f'Total (excl system): {today_supplier + today_customer}')
        
        mail.logout()
        return 0
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
