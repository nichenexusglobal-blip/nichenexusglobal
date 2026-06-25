"""Download attachments - fixed filename sanitization"""
import imaplib, email, os, base64, re
from email.header import decode_header

pwd = None
with open("C:/Users/leon/AppData/Local/hermes/profiles/nichenexusglobal/.env") as f:
    for line in f:
        if "EMAIL_PASSWORD" in line:
            pwd = line.split("=", 1)[1].strip()
            break

def sanitize(name):
    """Remove invalid Windows filename chars"""
    name = name.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    return name.strip()

def decode_filename(raw):
    try:
        decoded = decode_header(raw)
        return "".join([p.decode(c or "utf-8") if isinstance(p, bytes) else p for p, c in decoded])
    except:
        return raw

mail = imaplib.IMAP4_SSL("imap.exmail.qq.com", 993, timeout=15)
mail.login("pen@nichenexusglobal.com", pwd)
mail.select("INBOX")

save_dir = "C:/nichenexusglobal/attachments/supplier_docs"
os.makedirs(save_dir, exist_ok=True)

downloaded = []

# Bella (SOUOP)
status, ids = mail.search(None, '(FROM "bella@souoppowerstation.com")')
mids = ids[0].split()
print(f"Bella: scanning {len(mids)} emails for attachments")

for mid in mids[-1:]:
    status, data = mail.fetch(mid, "(RFC822)")
    if status != "OK": continue
    for part in data:
        if not isinstance(part, tuple): continue
        msg = email.message_from_bytes(part[1])
        date = msg.get("Date", "")
        print(f"\nEmail from Bella: {date}")
        
        if not msg.is_multipart(): continue
        for p in msg.walk():
            disp = str(p.get("Content-Disposition", ""))
            if "attachment" not in disp and "inline" not in disp:
                continue
            fn = p.get_filename()
            if not fn: continue
            
            fn = sanitize(decode_filename(fn))
            fpath = os.path.join(save_dir, fn)
            
            payload = p.get_payload(decode=True)
            if not payload:
                try:
                    payload = base64.b64decode(p.get_payload())
                except:
                    print(f"  ❌ Cannot decode: {fn}")
                    continue
            
            with open(fpath, "wb") as f:
                f.write(payload)
            size_kb = len(payload) / 1024
            print(f"  ✅ {fn} ({size_kb:.0f} KB)")
            downloaded.append(fpath)

# Pecron Chris - check for attachments too
print("\nPecron Chris:")
status, ids = mail.search(None, '(FROM "sales06@pecron.com")')
mids = ids[0].split()

for mid in mids[-3:]:
    status, data = mail.fetch(mid, "(RFC822)")
    if status != "OK": continue
    for part in data:
        if not isinstance(part, tuple): continue
        msg = email.message_from_bytes(part[1])
        date = msg.get("Date", "")
        
        if not msg.is_multipart(): continue
        for p in msg.walk():
            disp = str(p.get("Content-Disposition", ""))
            if "attachment" not in disp:
                continue
            fn = p.get_filename()
            if not fn: continue
            
            fn = sanitize(decode_filename(fn))
            fpath = os.path.join(save_dir, fn)
            
            payload = p.get_payload(decode=True)
            if not payload:
                try:
                    payload = base64.b64decode(p.get_payload())
                except:
                    print(f"  ❌ Cannot decode: {fn}")
                    continue
            
            with open(fpath, "wb") as f:
                f.write(payload)
            size_kb = len(payload) / 1024
            print(f"  ✅ {fn} ({size_kb:.0f} KB) from {date[:25]}")
            downloaded.append(fpath)

print(f"\n✅ 共下载 {len(downloaded)} 个文件到: {save_dir}")
for f in downloaded:
    print(f"  📎 {os.path.basename(f)}")
mail.close()
mail.logout()
