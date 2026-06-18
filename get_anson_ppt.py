#!/usr/bin/env python3
"""Download Anson Lee's PPT attachment"""
import imaplib, email, os

mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993)
mail.login('pen@nichenexusglobal.com', '4cd7vQ4GV59ATxxt')
mail.select('INBOX')

typ, data = mail.search(None, 'ALL')
ids = data[0].split()

os.makedirs('C:/nichenexusglobal/attachments', exist_ok=True)

for i in ids:
    typ, msg_data = mail.fetch(i, '(BODY.PEEK[HEADER.FIELDS (FROM)])')
    raw = msg_data[0][1]
    hdr = email.message_from_bytes(raw)
    fr = str(hdr.get('From', ''))
    
    if 'anson.le2002' in fr:
        typ2, msg_data2 = mail.fetch(i, '(RFC822)')
        raw2 = msg_data2[0][1]
        msg = email.message_from_bytes(raw2)
        
        for part in msg.walk():
            fn = part.get_filename()
            if fn:
                data = part.get_payload(decode=True)
                if data:
                    path = f'C:/nichenexusglobal/attachments/{fn}'
                    with open(path, 'wb') as f:
                        f.write(data)
                    print(f'Downloaded: {path} ({len(data)} bytes)')

mail.logout()
