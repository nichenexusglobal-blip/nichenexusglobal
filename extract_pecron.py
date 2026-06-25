"""Extract Pecron OEM picture from the .eml attachment"""
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

# Find Pecron's email with attachment
status, ids = mail.search(None, '(FROM "sales06@pecron.com")')
mids = ids[0].split()
print(f"Pecron: {len(mids)} emails")

# Get the latest ones
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
            
            # Decode filename
            try:
                decoded = decode_header(fn)
                fn = "".join([d.decode(c or "utf-8") if isinstance(d, bytes) else d for d, c in decoded])
            except:
                pass
            
            payload = p.get_payload(decode=True)
            if not payload:
                payload = p.get_payload()
                if isinstance(payload, str):
                    try:
                        payload = base64.b64decode(payload)
                    except:
                        pass
            
            if fn.endswith(".eml") or fn == "mail.eml":
                print(f"\n📧 Found .eml attachment from {date}")
                # Save the .eml first
                eml_path = os.path.join(save_dir, "pecron_nigeria.eml")
                with open(eml_path, "wb") as f:
                    f.write(payload if isinstance(payload, bytes) else payload.encode())
                print(f"  Saved: pecron_nigeria.eml ({os.path.getsize(eml_path)/1024:.0f} KB)")
                
                # Now parse the .eml to find images
                inner_msg = email.message_from_bytes(payload if isinstance(payload, bytes) else payload.encode())
                print(f"  Inner email subject: {inner_msg.get('Subject', '?')}")
                print(f"  Inner email from: {inner_msg.get('From', '?')}")
                
                if inner_msg.is_multipart():
                    for inner_part in inner_msg.walk():
                        ctype = inner_part.get_content_type()
                        if ctype.startswith("image/"):
                            img_data = inner_part.get_payload(decode=True)
                            if img_data:
                                ext = ctype.split("/")[-1]
                                img_name = f"pecron_nigeria_oem.{ext}"
                                img_path = os.path.join(save_dir, img_name)
                                with open(img_path, "wb") as f:
                                    f.write(img_data)
                                print(f"  🖼 Extracted image: {img_name} ({len(img_data)/1024:.0f} KB)")
                                
                                # Also try to get the filename from content-disposition
                                disp = str(inner_part.get("Content-Disposition", ""))
                                if "filename=" in disp:
                                    img_fn = disp.split("filename=")[-1].strip('"').strip("'")
                                    img_path2 = os.path.join(save_dir, img_fn)
                                    with open(img_path2, "wb") as f:
                                        f.write(img_data)
                                    print(f"  🖼 Also saved as: {img_fn}")
                
                # Also look for inline images in html parts
                if inner_msg.is_multipart():
                    for inner_part in inner_msg.walk():
                        if inner_part.get_content_type() == "text/html":
                            html = inner_part.get_payload(decode=True)
                            if html:
                                html_str = html.decode("utf-8", errors="replace")
                                # Look for embedded images (cid: references)
                                if "cid:" in html_str:
                                    print(f"  📎 Email has embedded images (cid references)")
            
            elif fn.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                filepath = os.path.join(save_dir, fn)
                with open(filepath, "wb") as f:
                    f.write(payload if isinstance(payload, bytes) else payload.encode())
                print(f"  🖼 Direct image: {fn} ({len(payload)/1024:.0f} KB) from {date[:25]}")

mail.close()
mail.logout()
