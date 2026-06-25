#!/usr/bin/env python3
"""Download attachments from supplier emails"""
import imaplib, email, sys, os, json, re
from email.header import decode_header

USER = 'pen@nichenexusglobal.com'
PASS = '4cd7vQ4GV59ATxxt'

ATTACH_DIR = '/c/nichenexusglobal/attachments_raw'

os.makedirs(ATTACH_DIR, exist_ok=True)

# Supplier domains we care about
TARGET_DOMS = [
    'pecron.com', 'anern.com', 'califepower.com', 'bloopower.com',
    'mecopower.com', 'shunxiangenergy.com', 'powerlfp.com', 'wpbattery.com',
    'piforz.com', 'taicopower.com', 'lansinestorage.com', 'ie-energy.com',
    'onesunpv.com', 'oukite'
]

try:
    mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993, timeout=30)
    mail.login(USER, PASS)
    mail.select('INBOX')
    
    status, data = mail.search(None, 'ALL')
    mids = data[0].split() if data[0] else []
    print(f"Total inbox: {len(mids)}", file=sys.stderr)
    
    # Process all emails, look for attachments from suppliers
    for mid in mids[-200:]:
        status, d = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])')
        if status != 'OK' or not d or not d[0]: continue
        try:
            raw = d[0][1]
            if isinstance(raw, bytes):
                hdr = raw.decode('utf-8', errors='replace')
            else:
                continue
        except:
            continue
        
        # Quick check if from supplier domain
        from_line = ''
        subj_line = ''
        for line in hdr.split('\n'):
            if line.startswith('From:'): from_line = line
            if line.startswith('Subject:'): subj_line = line
        
        if not any(dom in from_line.lower() for dom in TARGET_DOMS):
            continue
        if 'hermes agent' in subj_line.lower() or 'cronjob' in subj_line.lower():
            continue
        
        # Now get full message with attachment
        status2, d2 = mail.fetch(mid, '(RFC822)')
        if status2 != 'OK' or not d2 or not d2[0]: continue
        try:
            msg = email.message_from_bytes(d2[0][1])
        except:
            continue
        
        # Decode subject for filename
        subj = str(msg['Subject'] or 'no_subject')
        if '=?' in subj:
            try:
                sp = decode_header(subj)
                subj = ''
                for p, c in sp:
                    if isinstance(p, bytes):
                        subj += p.decode(c or 'utf-8', errors='replace')
                    else:
                        subj += str(p)
            except:
                pass
        
        # Sanitize subject for folder name
        safe_subj = re.sub(r'[^\w\-_ ]', '', subj)[:50].strip()
        from_addr = str(msg['From'] or 'unknown')
        supplier_name = from_addr.split('@')[0].strip('"\' ')
        # Sanitize supplier name for folder
        safe_name = re.sub(r'[^\w\-]', '_', supplier_name)[:30]
        supplier_folder = os.path.join(ATTACH_DIR, safe_name)
        os.makedirs(supplier_folder, exist_ok=True)
        
        # Walk parts for attachments
        att_count = 0
        if msg.is_multipart():
            for part in msg.walk():
                fn = part.get_filename()
                if not fn:
                    continue
                
                # Decode filename
                if '=?' in fn:
                    try:
                        sp = decode_header(fn)
                        fn = ''
                        for p, c in sp:
                            if isinstance(p, bytes):
                                fn += p.decode(c or 'utf-8', errors='replace')
                            else:
                                fn += str(p)
                    except:
                        pass
                
                payload = part.get_payload(decode=True)
                if not payload:
                    continue
                
                att_count += 1
                # Create unique filename
                base, ext = os.path.splitext(fn)
                if not ext:
                    ct = part.get_content_type()
                    if 'pdf' in ct: ext = '.pdf'
                    elif 'image' in ct: ext = '.jpg'
                    elif 'excel' in ct or 'spreadsheet' in ct: ext = '.xls'
                    elif 'word' in ct or 'document' in ct: ext = '.doc'
                
                fpath = os.path.join(supplier_folder, f"{att_count:02d}_{fn}")
                with open(fpath, 'wb') as f:
                    f.write(payload)
                
                filesize = len(payload)
                print(f"  📎 {supplier_name}/{fn} ({filesize/1024:.0f}KB)")
        
        # Also print body if useful
        body = ''
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                    except:
                        body = ''
                    break
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
            except:
                body = ''
        
        if body:
            lines = body.split('\n')
            clean = []
            for line in lines:
                s = line.strip()
                if s.startswith('>') or 'Original Message' in s:
                    break
                if s.startswith('From:') or s.startswith('Sent:') or s.startswith('Date:'):
                    continue
                clean.append(line)
            body_clean = '\n'.join(clean).strip()
            if body_clean:
                print(f"\n--- Body ({supplier_name}) ---")
                print(body_clean[:800])
    
    # Summary
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"Attachments saved to: {ATTACH_DIR}", file=sys.stderr)
    for root, dirs, files in os.walk(ATTACH_DIR):
        if files:
            print(f"  {os.path.basename(root)}/: {len(files)} files", file=sys.stderr)
            for f in files:
                fpath = os.path.join(root, f)
                sz = os.path.getsize(fpath)
                print(f"    {f} ({sz/1024:.0f}KB)", file=sys.stderr)
    
    mail.logout()

except Exception as e:
    sys.stderr.write(f"ERROR: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)
