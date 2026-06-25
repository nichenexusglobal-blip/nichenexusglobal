"""Check KWT Tech Mart bounce reason - was it 550 or temporary?"""
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

# Search for PostMaster bounces
status, ids = mail.search(None, '(FROM "PostMaster")')
mids = ids[0].split()
print(f"PostMaster emails: {len(mids)}")

for mid in mids[-3:]:
    status, data = mail.fetch(mid, "(RFC822)")
    if status != "OK": continue
    for part in data:
        if not isinstance(part, tuple): continue
        msg = email.message_from_bytes(part[1])
        date = msg.get("Date", "")
        subj = msg.get("Subject", "")
        
        try:
            decoded = decode_header(subj)
            subj = "".join([p.decode(c or "utf-8") if isinstance(p, bytes) else p for p, c in decoded])
        except:
            pass
        
        print(f"\n📧 {date}")
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
        
        # Check for 550 or other error codes
        if "550" in body:
            print("  ❌ 550 - 地址不存在（永久退信）")
        elif "5.1.1" in body or "user unknown" in body.lower():
            print("  ❌ 5.1.1 - 用户不存在")
        elif "5.4.1" in body or "relay" in body.lower():
            print("  ⚠️ 5.4.1 - 中继拒绝")
        elif "timeout" in body.lower() or "temporary" in body.lower():
            print("  ⚠️ 暂时性失败")
        
        print(f"\nBody (first 500):\n{body[:500]}")

mail.close()
mail.logout()
