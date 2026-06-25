#!/usr/bin/env python3
"""查已发送文件夹 — IMAP imap.exmail.qq.com"""
import imaplib
import email
from email.header import decode_header
import datetime

IMAP_SERVER = "imap.exmail.qq.com"
IMAP_PORT = 993
USER = "pen@nichenexusglobal.com"
PASSWORD = "4cd7v4QGV59ATxxt"

today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
today_str = today.strftime("%d-%b-%Y")

try:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(USER, PASSWORD)
    print("IMAP LOGIN OK")
    
    # Try different sent folder names
    sent_folders = ['"Sent Messages"', '"已发送"', '"Sent"', 'Sent', '已发送', '"Sent Items"']
    
    for folder in sent_folders:
        status, data = mail.select(folder)
        if status == 'OK':
            print(f"SENT folder found: {folder}")
            total = data[0].decode() if data else '?'
            print(f"Total sent: {total}")
            
            # Search today
            status, msg_ids = mail.search(None, f'(SINCE {today_str})')
            if status != 'OK':
                print(f"  Search failed: {status}")
                continue
            
            ids = msg_ids[0].split() if msg_ids[0] else []
            print(f"  Today's sent: {len(ids)}")
            
            supplier_count = 0
            customer_count = 0
            
            for mid in ids:
                status, data = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT TO DATE)])')
                if status != 'OK':
                    continue
                header_data = data[0][1] if len(data[0]) > 1 else b''
                msg = email.message_from_bytes(header_data)
                to_addr = msg.get('To', '')
                subj = msg.get('Subject', '')[:80]
                
                # Classify: supplier RFQ vs customer outreach
                supplier_kw = ['rfq', 'inquiry', 'fob', 'pricing', 'quote', '询盘', '报价']
                is_supplier = any(kw in subj.lower() for kw in supplier_kw)
                
                if is_supplier:
                    supplier_count += 1
                    cat = "SUPPLIER"
                else:
                    customer_count += 1
                    cat = "CUSTOMER"
                
                print(f"  [{cat}] To: {to_addr[:50]} | {subj}")
            
            print(f"\n=== TOTALS for {folder} ===")
            print(f"Supplier RFQs: {supplier_count}")
            print(f"Customer outreach: {customer_count}")
            print(f"Total sent today: {supplier_count + customer_count}")
            
            mail.logout()
            break
    else:
        print("No sent folder found with any name variant")
        # List all folders
        status, folders = mail.list()
        if status == 'OK':
            print("\nAvailable folders:")
            for f in folders:
                print(f"  {f}")
    
except imaplib.IMAP4.error as e:
    print(f"IMAP ERROR: {e}")
except Exception as e:
    print(f"ERROR: {e}")
