"""Read full content of important emails"""
import imaplib, email
from email.header import decode_header

pwd = None
with open("C:/Users/leon/AppData/Local/hermes/profiles/nichenexusglobal/.env") as f:
    for line in f:
        if "EMAIL_PASSWORD" in line:
            pwd = line.split("=", 1)[1].strip()
            break

mail = imaplib.IMAP4_SSL("imap.exmail.qq.com", 993, timeout=15)
mail.login("pen@nichenexusglobal.com", pwd)
mail.select("INBOX")

# Search for Bella (SOUOP) and Chris (Pecron)
search_from = ['(FROM "bella@souoppowerstation.com")', '(FROM "sales06@pecron.com")']

for sf in search_from:
    status, ids = mail.search(None, sf)
    mids = ids[0].split()
    print(f"\n{'='*60}")
    print(f"搜索: {sf} → {len(mids)} 封")
    
    for mid in mids[-5:]:  # latest 5
        status, data = mail.fetch(mid, "(RFC822)")
        if status != "OK":
            continue
        for part in data:
            if isinstance(part, tuple):
                msg = email.message_from_bytes(part[1])
                fr = msg.get("From", "")
                subj = msg.get("Subject", "")
                date = msg.get("Date", "")
                
                print(f"\n📧 {date}")
                print(f"From: {fr}")
                print(f"Subj: {subj}")
                
                # Get body
                body = ""
                if msg.is_multipart():
                    for p in msg.walk():
                        if p.get_content_type() == "text/plain":
                            try:
                                body = p.get_payload(decode=True).decode("utf-8", errors="replace")
                            except:
                                body = str(p.get_payload(decode=True))
                            break
                else:
                    try:
                        body = msg.get_payload(decode=True).decode("utf-8", errors="replace")
                    except:
                        body = str(msg.get_payload())
                
                # Print first 2000 chars
                print(f"Body:\n{body[:2000]}")
                if len(body) > 2000:
                    print(f"\n... ({len(body)} chars total)")

mail.close()
mail.logout()
