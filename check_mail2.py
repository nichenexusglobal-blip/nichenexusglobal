"""Check email inbox — use password from .env like the successful diag"""
import imaplib, email
from email.header import decode_header

# Read password from .env (same method that worked in diag)
pwd = None
with open("C:/Users/leon/AppData/Local/hermes/profiles/nichenexusglobal/.env") as f:
    for line in f:
        if "EMAIL_PASSWORD" in line:
            pwd = line.split("=", 1)[1].strip()
            break

if not pwd:
    print("❌ No password found in .env")
    exit(1)

# Connect
mail = imaplib.IMAP4_SSL("imap.exmail.qq.com", 993, timeout=15)
mail.login("pen@nichenexusglobal.com", pwd)
print("✅ IMAP login OK")

mail.select("INBOX")

# Search recent (last 4 days)
status, ids = mail.search(None, 'SINCE 21-Jun-2026')
all_ids = ids[0].split()
print(f"📬 {len(all_ids)} emails since Jun 21")

recent = all_ids[-40:]
system_from = ["hermes@nousresearch.com", "noreply@github.com", "mailer-daemon@", "postmaster@"]

real_emails = []
sys_count = 0

for mid in reversed(recent):
    status, data = mail.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
    if status != "OK":
        continue
    for part in data:
        if isinstance(part, tuple):
            try:
                msg = email.message_from_bytes(part[1])
                fr = msg.get("From", "")
                subj = msg.get("Subject", "")
                date = msg.get("Date", "")
                
                try:
                    decoded = decode_header(subj)
                    subj = "".join([p.decode(c or "utf-8") if isinstance(p, bytes) else p for p, c in decoded])
                except:
                    pass
                
                fr_lower = fr.lower()
                if any(s in fr_lower for s in system_from):
                    sys_count += 1
                    continue
                
                real_emails.append({"from": fr, "subject": subj, "date": date})
            except:
                continue

print(f"   System: {sys_count}")
print(f"   Real: {len(real_emails)}")
print()

for e in real_emails:
    print(f"📧 {e['date'][:25]}")
    print(f"   From: {e['from']}")
    print(f"   Subj: {e['subject'][:120]}")
    print()

mail.close()
mail.logout()
