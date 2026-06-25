#!/usr/bin/env python3
"""Check today's (June 22) inbound emails - real non-system ones"""
import imaplib
import email
from email.header import decode_header

def decode_subj(s):
    if not s: return ''
    parts = decode_header(s)
    result = []
    for part, charset in parts:
        if isinstance(part, bytes):
            try:
                result.append(part.decode(charset or 'utf-8', errors='replace'))
            except:
                result.append(part.decode('utf-8', errors='replace'))
        else:
            result.append(part)
    return ''.join(result)

m = imaplib.IMAP4_SSL('imap.exmail.qq.com')
m.login('pen@nichenexusglobal.com', '4cd7vQ4GV59ATxxt')
m.select('INBOX')
st, ids = m.search(None, 'ALL')
all_ids = ids[0].split()
print(f'Total inbox: {len(all_ids)}')

today_count = 0
for mid in reversed(all_ids[-400:]):
    st, data = m.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE TO)])')
    if st != 'OK': continue
    msg = email.message_from_bytes(data[0][1])
    dt = msg.get('Date', '')
    if '22 Jun 2026' in dt:
        frm = msg.get('From', '') or ''
        subj = decode_subj(msg.get('Subject', ''))
        to = msg.get('To', '') or ''
        # Skip system emails
        if 'pen@nichenexusglobal.com' in frm:
            continue
        if 'Hermes Agent' in subj or 'Cronjob' in subj:
            continue
        today_count += 1
        print(f'\n--- Email #{today_count} ---')
        print(f'From: {frm[:80]}')
        print(f'Subj: {subj[:100]}')
        print(f'Date: {dt}')
        # Fetch body
        st2, data2 = m.fetch(mid, '(BODY.PEEK[TEXT])')
        if st2 == 'OK':
            body = data2[0][1]
            if isinstance(body, bytes):
                body_text = body.decode('utf-8', errors='replace')[:500]
            else:
                body_text = str(body)[:500]
            print(f'Body preview: {body_text}')
        print()

if today_count == 0:
    print("No non-system real emails from today (June 22) found.")

print(f'\nTotal real non-system emails today: {today_count}')
m.logout()
