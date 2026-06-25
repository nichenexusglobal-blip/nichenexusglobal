#!/usr/bin/env python3
"""Fetch and decode the Pecron Chris email from June 22"""
import imaplib
import email
import base64

m = imaplib.IMAP4_SSL('imap.exmail.qq.com')
m.login('pen@nichenexusglobal.com', '4cd7vQ4GV59ATxxt')
m.select('INBOX')
st, ids = m.search(None, 'ALL')
all_ids = ids[0].split()

for mid in reversed(all_ids[-400:]):
    st, data = m.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
    if st != 'OK': continue
    msg = email.message_from_bytes(data[0][1])
    dt = msg.get('Date', '')
    if '22 Jun 2026' in dt:
        frm = msg.get('From', '') or ''
        if 'pecron' in frm.lower():
            # Fetch full body
            st2, data2 = m.fetch(mid, '(RFC822)')
            if st2 == 'OK':
                raw_msg = email.message_from_bytes(data2[0][1])
                print(f"=== FULL EMAIL ===")
                print(f"From: {frm}")
                print(f"Subject: {msg.get('Subject','')}")
                print(f"Date: {dt}")
                print()
                # Get body
                if raw_msg.is_multipart():
                    for part in raw_msg.walk():
                        ct = part.get_content_type()
                        if ct == 'text/plain':
                            payload = part.get_payload(decode=True)
                            if payload:
                                print("--- TEXT BODY ---")
                                print(payload.decode('utf-8', errors='replace'))
                                break
                else:
                    payload = raw_msg.get_payload(decode=True)
                    if payload:
                        print("--- BODY ---")
                        print(payload.decode('utf-8', errors='replace'))
            break

m.logout()
