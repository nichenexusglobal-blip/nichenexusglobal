#!/usr/bin/env python3
"""Check all supplier emails - extract FOB prices, MOQ, shipping info"""
import imaplib, email, json, re
from email.header import decode_header

USER = 'pen@nichenexusglobal.com'
PASS = '4cd7vQ4GV59ATxxt'

mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993)
mail.login(USER, PASS)
mail.select('INBOX')

# Get all messages
status, data = mail.search(None, 'ALL')
msg_ids = data[0].split() if data[0] else []
print(f"Total inbox: {len(msg_ids)}")

# We need to look for supplier-related emails
# Keywords to match supplier emails
SUPPLIER_KEYWORDS = [
    'quote', 'quotation', 'quotation', '报价', 'FOB', 'EXW', 'price',
    'catalog', 'catalogue', '目录', '产品目录', 'PI', 'proforma',
    'invoice', 'delivery', 'shipping', 'MOQ', 'sample',
    'certificate', 'cert', 'CE', 'FCC', 'UN38.3', 'RoHS',
    'anern', 'pecron', 'meco', 'piforz', 'shunxiang', 'ie-energy',
    'powerlfp', 'worldpower', 'allpowers', 'taico', 'lansine',
    'sinorise', 'hangcheng', 'jieyang', 'calife', 'oneSun',
    'luke', 'chris', 'factory', 'manufacturer', 'supplier',
    'battery', 'power station', 'solar', 'inverter',
    'sample', 'shipment', 'tracking', 'order', 'payment',
    'alibaba', 'trade assurance',
    # Common Chinese supplier email patterns
    'solar', 'energy', 'power', 'battery', 'lighting', 'led',
]

# Check last 200 messages (most recent)
recent = msg_ids[-200:]
supplier_emails = []

for mid in recent:
    status, data = mail.fetch(mid, '(RFC822)')
    if status != 'OK': continue
    if not data or not data[0]: continue
    try:
        msg = email.message_from_bytes(data[0][1])
    except (TypeError, IndexError):
        continue
    
    # Decode subject
    subj_parts = decode_header(msg['Subject'] or '')
    subj = ''
    for part, charset in subj_parts:
        if isinstance(part, bytes):
            subj += part.decode(charset or 'utf-8', errors='replace')
        else:
            subj += part
    
    from_ = str(msg['From'] or '')
    date_ = str(msg['Date'] or '')
    
    # Get body text
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
    
    # Check if this looks like a supplier email
    text_to_check = (subj + ' ' + from_ + ' ' + body[:500]).lower()
    is_supplier = any(kw.lower() in text_to_check for kw in SUPPLIER_KEYWORDS)
    
    # Always check for price numbers
    has_price = bool(re.search(r'\$\s*\d+\.?\d*', text_to_check))
    
    if is_supplier or has_price:
        # Get attachments info
        attachments = []
        if msg.is_multipart():
            for part in msg.walk():
                fn = part.get_filename()
                if fn:
                    attachments.append(fn)
        
        supplier_emails.append({
            'from': from_,
            'subject': subj[:200],
            'date': date_,
            'has_price': has_price,
            'is_supplier': is_supplier,
            'attachments': attachments,
            'body_preview': body[:500].strip()
        })

mail.logout()

print(f"\n=== SUPPLIER-RELATED EMAILS FOUND: {len(supplier_emails)} ===\n")

for i, e in enumerate(supplier_emails):
    print(f"[{i+1}] {e['date']}")
    print(f"    From: {e['from'][:80]}")
    print(f"    Subj: {e['subject'][:100]}")
    if e['attachments']:
        print(f"    Attachments: {', '.join(e['attachments'])}")
    print(f"    Price: {'💰 YES' if e['has_price'] else 'No price'}")
    print(f"    Supplier: {'✅' if e['is_supplier'] else '⚠️'}")
    preview = e['body_preview'][:200].replace('\n', ' | ')
    print(f"    Preview: {preview}")
    print()
