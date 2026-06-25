"""Extract Pecron OEM picture - fixed"""
import imaplib, email, os, base64
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

save_dir = "C:/nichenexusglobal/attachments/supplier_docs"
os.makedirs(save_dir, exist_ok=True)

status, ids = mail.search(None, '(FROM "sales06@pecron.com")')
mids = ids[0].split()

for mid in mids[-5:]:
    status, data = mail.fetch(mid, "(RFC822)")
    if status != "OK": continue
    for part in data:
        if not isinstance(part, tuple): continue
        msg = email.message_from_bytes(part[1])
        date = msg.get("Date", "")
        
        if not msg.is_multipart(): continue
        for p in msg.walk():
            fn = p.get_filename()
            if not fn: continue
            
            try:
                decoded = decode_header(fn)
                fn = "".join([d.decode(c or "utf-8") if isinstance(d, bytes) else d for d, c in decoded])
            except:
                pass
            
            payload = p.get_payload(decode=True)
            if payload is None:
                # Try non-decoded
                raw = p.get_payload()
                if isinstance(raw, list):
                    # Multipart - try each subpart
                    for sub in raw:
                        if isinstance(sub, str):
                            try:
                                payload = base64.b64decode(sub)
                                break
                            except:
                                pass
                elif isinstance(raw, str):
                    try:
                        payload = base64.b64decode(raw)
                    except:
                        pass
            
            if payload is None:
                continue
            
            if fn.endswith(".eml") or fn == "mail.eml":
                print(f"📧 Found .eml from {date}")
                
                # Write .eml file
                eml_path = os.path.join(save_dir, "pecron_nigeria.eml")
                with open(eml_path, "wb") as f:
                    f.write(payload if isinstance(payload, bytes) else payload.encode("utf-8"))
                print(f"  Saved: pecron_nigeria.eml ({os.path.getsize(eml_path)/1024:.0f} KB)")
                
                # Parse inner email for images
                try:
                    inner = email.message_from_bytes(payload if isinstance(payload, bytes) else payload.encode())
                    if inner.is_multipart():
                        for sub in inner.walk():
                            if sub.get_content_type().startswith("image/"):
                                img = sub.get_payload(decode=True)
                                if img:
                                    ext = sub.get_content_type().split("/")[-1]
                                    img_path = os.path.join(save_dir, f"pecron_nigeria_oem.{ext}")
                                    with open(img_path, "wb") as f:
                                        f.write(img)
                                    print(f"  🖼 OEM image extracted: pecron_nigeria_oem.{ext} ({len(img)/1024:.0f} KB)")
                except Exception as e:
                    print(f"  ❌ Could not parse inner email: {e}")
            
            elif fn.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                fpath = os.path.join(save_dir, fn)
                with open(fpath, "wb") as f:
                    f.write(payload)
                print(f"  🖼 Image: {fn} ({len(payload)/1024:.0f} KB)")

mail.close()
mail.logout()
print("\n✅ Done")
