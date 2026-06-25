#!/usr/bin/env python3
"""Check sent messages - count today's sends and categorize them"""
import imaplib
import email
import sys

def main():
    try:
        mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993)
        mail.login('pen@nichenexusglobal.com', '4cd7vQ4GV59ATxxt')
        
        # List folders to find Sent
        resp, folders = mail.list()
        sent_folder = None
        for f in folders:
            s = f.decode() if isinstance(f, bytes) else f
            if '\u5df2\u53d1\u9001' in s or 'Sent Messages' in s:
                sent_folder = s.split(' "/" ')[-1].strip('"') if ' "/" ' in s else s
                # Extract folder name
                parts = s.split(' "/" ')
                if len(parts) > 1:
                    folder_name = parts[-1].strip('"')
                else:
                    continue
                sent_folder = folder_name
                break
        
        if not sent_folder:
            print('Could not find Sent folder')
            # Try common names
            for name in ['Sent Messages', '\u5df2\u53d1\u9001', 'Sent', 'Sent Items']:
                print(f'Trying: {name}')
                status, data = mail.select(f'"{name}"')
                if status == 'OK':
                    sent_folder = name
                    break
        
        if not sent_folder:
            print('ERROR: No sent folder found')
            return 1
        
        print(f'Using folder: {sent_folder}')
        status, data = mail.select(f'"{sent_folder}"')
        print(f'Select result: {status} {data}')
        
        if status != 'OK':
            print(f'Failed to select sent folder')
            return 1
        
        status, ids = mail.search(None, 'ALL')
        if status != 'OK':
            print('No messages in sent folder')
            return 0
            
        all_ids = ids[0].split()
        total_sent = len(all_ids)
        print(f'Sent Messages total: {total_sent}')
        
        # Scan recent 200 messages for today
        recent_ids = all_ids[-200:] if total_sent > 200 else all_ids
        today_msgs = []
        supplier_count = 0
        customer_count = 0
        
        for mid in reversed(recent_ids):
            status, data = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE TO)])')
            if status != 'OK':
                continue
            msg = email.message_from_bytes(data[0][1])
            dt = msg.get('Date', '')
            subj = msg.get('Subject', '') or ''
            to = msg.get('To', '') or ''
            
            # Check if today (UTC+8 2026-06-19)
            if '19 Jun 2026' in dt:
                today_msgs.append((to.strip(), subj.strip(), dt.strip()))
                # Categorize
                lower_subj = subj.lower()
                lower_to = to.lower()
                if any(k in lower_subj for k in ['rfq', 'inquiry', 'pricing', 'fob', 'quote', 'supplier']):
                    supplier_count += 1
                elif any(k in lower_to for k in ['@alibaba.com', 'rfq']):
                    supplier_count += 1
                else:
                    customer_count += 1
        
        print(f'\n=== TODAY ({len(today_msgs)} messages) ===')
        for to, subj, dt in today_msgs:
            print(f'  To: {to[:50]} | Subj: {subj[:60]} | Date: {dt}')
        
        print(f'\n--- Summary ---')
        print(f'Today total sent: {len(today_msgs)}')
        print(f'  Supplier RFQs: {supplier_count}')
        print(f'  Customer outreach: {customer_count}')
        
        mail.logout()
        return 0
    except Exception as e:
        print(f'IMAP ERROR: {e}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
