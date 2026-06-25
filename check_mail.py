"""Check email inbox for new replies"""
import imaplib, email, json
from email.header import decode_header

# Connect
mail = imaplib.IMAP4_SSL("imap.exmail.qq.com", 993)
try:
    mail.login("pen@nichenexusglobal.com", "4cd7v4QGV59ATxxt")
    print("✅ IMAP login OK")
except Exception as e:
    print(f"❌ Login failed: {e}")
    exit(1)

# Select inbox
mail.select("INBOX")

# Search for recent (last 3 days)
status, ids = mail.search(None, 'SINCE 22-Jun-2026')
if status != "OK":
    print(f"❌ Search failed: {status}")
    exit(1)

all_ids = ids[0].split()
print(f"📬 共 {len(all_ids)} 封邮件（6月22日至今）")

# Get latest 30
recent = all_ids[-30:]
print(f"📬 最近30封：")

system_from = ["hermes@nousresearch.com", "noreply@github.com", "mailer-daemon@"]

real_emails = []
system_count = 0

for mid in reversed(recent):
    status, data = mail.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
    if status != "OK":
        continue
    for part in data:
        if isinstance(part, tuple):
            try:
                msg = email.message_from_bytes(part[1])
                fr = msg.get("From", "")
                subject = msg.get("Subject", "")
                date = msg.get("Date", "")
                
                # Decode subject
                try:
                    decoded_parts = decode_header(subject)
                    subject = "".join([p.decode(charset or "utf-8") if isinstance(p, bytes) else p for p, charset in decoded_parts])
                except:
                    pass
                
                # Check if system email
                is_system = any(s in fr.lower() for s in system_from)
                
                if is_system:
                    system_count += 1
                    continue
                
                real_emails.append({"from": fr, "subject": subject, "date": date})
            except:
                continue

print(f"\n📬 系统邮件: {system_count}封")
print(f"📬 真实邮件: {len(real_emails)}封")
print()
for e in real_emails:
    print(f"{e['date'][:25]}")
    print(f"  From: {e['from']}")
    print(f"  Subj: {e['subject'][:100]}")
    print()

mail.close()
mail.logout()
