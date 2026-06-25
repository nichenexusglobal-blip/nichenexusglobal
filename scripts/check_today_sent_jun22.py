#!/usr/bin/env python3
"""Check today's (June 22) sent messages from Sent folder"""
import imaplib
import email

m = imaplib.IMAP4_SSL('imap.exmail.qq.com')
m.login('pen@nichenexusglobal.com', '4cd7vQ4GV59ATxxt')
m.select('"Sent Messages"')
st, ids = m.search(None, 'ALL')
all_ids = ids[0].split()
print(f'Total sent: {len(all_ids)}')
today_count = 0
supplier_count = 0
customer_count = 0

for mid in reversed(all_ids[-500:]):
    st, data = m.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE TO)])')
    if st != 'OK':
        continue
    msg = email.message_from_bytes(data[0][1])
    dt = msg.get('Date', '')
    if '22 Jun 2026' in dt:
        today_count += 1
        subj = msg.get('Subject', '') or ''
        to_addr = msg.get('To', '') or ''
        print(f'  To: {to_addr[:80]}')
        print(f'  Subj: {subj[:100]}')
        print(f'  Date: {dt}')
        lower_subj = subj.lower()
        if any(k in lower_subj for k in ['rfq', 'inquiry', 'pricing', 'fob', 'quote', 'supplier']):
            supplier_count += 1
        else:
            customer_count += 1
        print()

print(f'--- Summary ---')
print(f'Today total sent (June 22): {today_count}')
print(f'  Supplier RFQs: {supplier_count}')
print(f'  Customer outreach: {customer_count}')
m.logout()
