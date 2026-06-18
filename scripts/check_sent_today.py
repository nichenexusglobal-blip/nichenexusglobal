#!/usr/bin/env python3
"""Step 2: Check today's sent folder — count and categorize emails."""
import imaplib, email, os
from email.header import decode_header
from datetime import datetime, timezone, timedelta
import re

TZ = timezone(timedelta(hours=8))
today = datetime.now(TZ)

def decode_str(s):
    if s is None: return ''
    parts = decode_header(s)
    result = []
    for part, charset in parts:
        if isinstance(part, bytes):
            try: result.append(part.decode(charset or 'utf-8', errors='replace'))
            except: result.append(part.decode('utf-8', errors='replace'))
        else: result.append(str(part))
    return ''.join(result)

mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993)
mail.login('pen@nichenexusglobal.com', os.environ.get('NICHE_EMAIL_PASSWORD', ''))

# Try different folder names
folders_to_try = ['"Sent Messages"', '"已发送"', 'Sent', 'INBOX.Sent']

for folder in folders_to_try:
    try:
        s, d = mail.select(folder)
        if s == 'OK':
            print(f"✅ Found folder: {folder}")
            break
    except:
        continue
else:
    # Try listing all folders
    s, folders = mail.list()
    print("Available folders:")
    for f in folders:
        print(f"  {f.decode('utf-8', errors='replace')}")
    mail.logout()
    exit(1)

# Today's sent
s, d = mail.search(None, f'SINCE {today.strftime("%d-%b-%Y")}')
today_ids = d[0].split() if d[0] else []
print(f"\nToday ({today.strftime('%Y-%m-%d')}) sent count: {len(today_ids)}")

supplier_count = 0
customer_count = 0
with_quote_count = 0
without_quote_count = 0
self_count = 0  # count emails to self/pen@
other_count = 0

supplier_keywords = ['rfq', 'inquiry', 'quote', '询盘', '询价', 'supplier', 'manufacturer', 'factory', 'OEM']
customer_keywords = ['distributor', 'reseller', 'wholesale', 'partner', 'pricing', 'private label', 'brand']

for i, mid in enumerate(today_ids):
    s, data = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM TO SUBJECT DATE)])')
    if s != 'OK':
        continue
    raw = data[0][1].decode('utf-8', errors='replace')
    
    to_line = ''
    subj_line = ''
    for l in raw.split('\n'):
        if l.startswith('To:'):
            to_line = l[4:].strip()
        if l.startswith('Subject:'):
            subj_line = l[9:].strip()
    
    subj_decoded = decode_str(subj_line) if subj_line else ''
    to_decoded = decode_str(to_line) if to_line else ''
    
    # Skip emails to self
    if 'pen@nichenexusglobal.com' in to_decoded.lower():
        self_count += 1
        continue
    
    # Check if it's a supplier inquiry
    is_supplier = any(kw in subj_decoded.lower() or kw in to_decoded.lower() for kw in supplier_keywords)
    
    # Check if it has a quote
    has_price = any(kw in subj_decoded.lower() for kw in ['quote', '报价', 'pricing'])
    
    print(f"{i+1}. TO: {to_decoded[:70]} | SUBJ: {subj_decoded[:100]} | {'SUPPLIER' if is_supplier else 'CLIENT'} | {'HAS_PRICE' if has_price else 'NO_PRICE'}")
    
    if is_supplier:
        supplier_count += 1
    else:
        customer_count += 1
        if has_price:
            with_quote_count += 1
        else:
            without_quote_count += 1

print(f"\n{'='*50}")
print(f"TOTAL sent today (excluding self): {len(today_ids) - self_count}")
print(f"  Supplier verification: {supplier_count}")
print(f"  Customer outreach: {customer_count}")
print(f"    With quote: {with_quote_count}")
print(f"    Without quote (empty nail): {without_quote_count}")
print(f"  Self/admin: {self_count}")
print(f"  Total: {len(today_ids)}")

mail.close()
mail.logout()
