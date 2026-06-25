"""Check Pecron email for inline embedded images"""
import imaplib, email, os, re
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

# Get the latest email from Pecron (June 23)
for mid in mids[-2:]:
    status, data = mail.fetch(mid, "(RFC822)")
    if status != "OK": continue
    for part in data:
        if not isinstance(part, tuple): continue
        msg = email.message_from_bytes(part[1])
        date = msg.get("Date", "")
        
        print(f"\n📧 {date}")
        print(f"Subject: {msg.get('Subject', '?')}")
        
        # Walk all parts looking for inline images
        inline_images = []
        for p in msg.walk():
            ctype = p.get_content_type()
            cid = p.get("Content-ID", "")
            disp = str(p.get("Content-Disposition", ""))
            
            if ctype.startswith("image/"):
                payload = p.get_payload(decode=True)
                if payload:
                    # Save with CID or filename
                    cid_clean = cid.strip("<>") if cid else "inline"
                    fn = p.get_filename() or f"pecron_inline_{cid_clean}.{ctype.split('/')[-1]}"
                    
                    try:
                        decoded = decode_header(fn)
                        fn = "".join([d.decode(c or "utf-8") if isinstance(d, bytes) else d for d, c in decoded])
                    except:
                        pass
                    
                    fpath = os.path.join(save_dir, fn)
                    with open(fpath, "wb") as f:
                        f.write(payload)
                    print(f"  🖼 {fn} ({len(payload)/1024:.0f} KB) - inline={bool(cid)}")
                    inline_images.append(fpath)
            
            # Look for HTML body with embedded b64 images
            if ctype == "text/html":
                html = p.get_payload(decode=True)
                if html:
                    html_str = html.decode("utf-8", errors="replace")
                    # Find base64 embedded images
                    matches = re.findall(r'<img[^>]+src="data:image/([^;]+);base64,([^"]+)"', html_str)
                    for ext, b64data in matches:
                        try:
                            img_data = base64.b64decode(b64data)
                            fpath = os.path.join(save_dir, f"pecron_embedded.{ext}")
                            with open(fpath, "wb") as f:
                                f.write(img_data)
                            print(f"  🖼 Embedded image (base64 in HTML): {len(img_data)/1024:.0f} KB")
                        except:
                            pass
                    
                    # Also check for cid references
                    cids = re.findall(r'cid:([^"\'>]+)', html_str)
                    if cids:
                        print(f"  📎 References inline images: {cids}")

if not inline_images:
    print("\n⚠️ No images found as attachments or inline in Pecron emails.")
    print("  Chris said 'I sent you the picture' - it may have been")
    print("  sent in a different email or the image was stripped by")
    print("  the mail server.")

mail.close()
mail.logout()
