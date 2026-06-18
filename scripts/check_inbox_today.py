#!/usr/bin/env python3
"""Check today's inbox and sent messages via IMAP."""
import imaplib
import email
from email.header import decode_header
import ssl
from datetime import datetime, timezone, timedelta

imap_server = "imap.exmail.qq.com"
imap_port = 993
username = "pen@nichenexusglobal.com"
password = "4cd7v4QGV59ATxxt"

tz_utc8 = timezone(timedelta(hours=8))
today_start = datetime.now(tz_utc8).replace(hour=0, minute=0, second=0, microsecond=0)
print(f"Today (UTC+8): {today_start.strftime('%Y-%m-%d %H:%M:%S')}")

try:
    ctx = ssl.create_default_context()
    mail = imaplib.IMAP4_SSL(imap_server, imap_port, ssl_context=ctx)
    mail.login(username, password)
    print("IMAP LOGIN SUCCESS")

    # List all mailboxes
    status, mailboxes = mail.list()
    print(f"\n=== All mailboxes ===")
    for mb in mailboxes:
        print(mb.decode('utf-8', errors='replace'))

    # === INBOX ===
    status, data = mail.select("INBOX")
    print(f"\nINBOX select status: {status}")
    total_msgs = data[0] if data else b'0'
    print(f"Total INBOX messages: {total_msgs.decode()}")

    date_str = today_start.strftime("%d-%b-%Y")
    print(f"\n=== Searching INBOX since {date_str} ===")
    status, msg_ids = mail.search(None, f'SINCE {date_str}')
    if status == 'OK':
        ids = msg_ids[0].split()
        print(f"Found {len(ids)} messages since {date_str}")

        for i, msg_id in enumerate(ids[:30]):
            status, msg_data = mail.fetch(msg_id, '(RFC822)')
            if status != 'OK':
                continue
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Subject
            subject = ""
            if msg['Subject']:
                decoded_parts = decode_header(msg['Subject'])
                subject = ''.join(
                    part.decode(enc or 'utf-8') if isinstance(part, bytes) else part
                    for part, enc in decoded_parts
                )

            from_addr = msg['From'] or "unknown"
            date_val = msg['Date'] or "unknown"

            # Body preview
            body_preview = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        payload = part.get_payload(decode=True)
                        if payload:
                            body_preview = payload.decode('utf-8', errors='replace')[:400]
                        break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body_preview = payload.decode('utf-8', errors='replace')[:400]

            print(f"\n--- Inbox Email {i+1} ---")
            print(f"From: {from_addr}")
            print(f"Subject: {subject}")
            print(f"Date: {date_val}")
            print(f"Body preview: {body_preview}")

    # === SENT MESSAGES ===
    print(f"\n\n=== Trying Sent Messages ===")
    # The Sent Messages folder might have different names
    # Try multiple variants
    for folder_name in ['"Sent Messages"', '"Sent"', '"已发送"', '"Sent Items"']:
        try:
            status, data = mail.select(folder_name)
            print(f"Tried '{folder_name}': status={status}, data={data}")
            if status == 'OK':
                break
        except:
            continue

    if status == 'OK':
        status, msg_ids = mail.search(None, f'SINCE {date_str}')
        if status == 'OK':
            ids = msg_ids[0].split()
            print(f"Found {len(ids)} sent messages since {date_str}")

            supplier_count = 0
            customer_count = 0
            total_sent = 0

            for i, msg_id in enumerate(ids[:100]):
                status, msg_data = mail.fetch(msg_id, '(RFC822)')
                if status != 'OK':
                    continue
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                subject = ""
                if msg['Subject']:
                    decoded_parts = decode_header(msg['Subject'])
                    subject = ''.join(
                        part.decode(enc or 'utf-8') if isinstance(part, bytes) else part
                        for part, enc in decoded_parts
                    )
                to_addr = msg['To'] or "unknown"
                date_val = msg['Date'] or "unknown"
                total_sent += 1

                # Classify
                subj_lower = subject.lower()
                if any(kw in subj_lower for kw in ['rfq', 'inquiry', 'quote', '询盘', '供应商']):
                    category = "supplier"
                    supplier_count += 1
                elif any(kw in subj_lower for kw in ['supply', 'partnership', 'pricing', 'oem', 'wholesale']):
                    category = "customer"
                    customer_count += 1
                else:
                    category = "other"
                    if subj_lower:
                        customer_count += 1
                    else:
                        category = "unknown"

                print(f"\n  Sent {i+1}: To={to_addr} | [{category}] {subject[:90]} | Date={date_val}")

            print(f"\n=== SENT SUMMARY ===")
            print(f"Total today: {total_sent}")
            print(f"Supplier RFQs: {supplier_count}")
            print(f"Customer outreach: {customer_count}")
            print(f"Other: {total_sent - supplier_count - customer_count}")

    mail.logout()

except imaplib.IMAP4.error as e:
    print(f"\nIMAP ERROR: {e}")
    print("This is the known issue with exmail.qq.com IMAP.")
    print("Cannot read inbox today. Reporting as '无法读收件箱'.")
except Exception as e:
    print(f"\nOTHER ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
