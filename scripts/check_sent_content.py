#!/usr/bin/env python3
"""Check today's sent emails for pricing/quote content"""
import imaplib
import email

m = imaplib.IMAP4_SSL('imap.exmail.qq.com')
m.login('pen@nichenexusglobal.com', '4cd7vQ4GV59ATxxt')
m.select('"Sent Messages"')
st, ids = m.search(None, 'ALL')
all_ids = ids[0].split()

for mid in reversed(all_ids[-500:]):
    st, data = m.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE TO)])')
    if st != 'OK': continue
    msg = email.message_from_bytes(data[0][1])
    dt = msg.get('Date', '')
    if '22 Jun 2026' in dt:
        to_addr = (msg.get('To', '') or '').strip()
        # Skip internal (pen@)
        if 'pen@nichenexusglobal.com' in to_addr:
            continue
        subj = msg.get('Subject', '') or ''
        print(f"=== External: To: {to_addr} ===")
        print(f"Subj: {subj}")
        # Fetch full email
        st2, data2 = m.fetch(mid, '(RFC822)')
        if st2 == 'OK':
            raw_msg = email.message_from_bytes(data2[0][1])
            if raw_msg.is_multipart():
                for part in raw_msg.walk():
                    ct = part.get_content_type()
                    if ct == 'text/plain':
                        payload = part.get_payload(decode=True)
                        if payload:
                            body = payload.decode('utf-8', errors='replace')[:1000]
                            print(f"Body:\n{body}")
                            break
            else:
                payload = raw_msg.get_payload(decode=True)
                if payload:
                    print(f"Body:\n{payload.decode('utf-8', errors='replace')[:1000]}")
        print("\n---\n")

m.logout()
