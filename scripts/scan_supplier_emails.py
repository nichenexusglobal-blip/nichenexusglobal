#!/usr/bin/env python3
"""Quick supplier email scan - last 100 messages only"""
import imaplib, email, re, sys, json
from email.header import decode_header
import traceback

USER = 'pen@nichenexusglobal.com'
PASS = '4cd7vQ4GV59ATxxt'

try:
    mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993, timeout=20)
    mail.login(USER, PASS)
    mail.select('INBOX')
    
    status, data = mail.search(None, 'ALL')
    msg_ids = data[0].split() if data[0] else []
    sys.stderr.write(f"Total: {len(msg_ids)}\n")
    
    recent = msg_ids[-80:]
    results = []
    
    for mid in recent:
        status, d = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
        if status != 'OK': continue
        if not d or not d[0]: continue
        try:
            raw = d[0][1]
            if isinstance(raw, bytes):
                msg = email.message_from_bytes(raw)
            else:
                continue
        except:
            continue
        
        subj_parts = decode_header(msg['Subject'] or '')
        subj = ''
        for part, charset in subj_parts:
            if isinstance(part, bytes):
                subj += part.decode(charset or 'utf-8', errors='replace')
            else:
                subj += str(part)
        
        from_ = str(msg['From'] or '')
        date_ = str(msg['Date'] or '')
        
        # Check if supplier-related
        text = (subj + ' ' + from_).lower()
        kw = ['quote','quotation','fob','exw','price','catalog','moq',
              'sample','pi','proforma','invoice','delivery','shipping',
              'anern','pecron','meco','piforz','shunxiang','ie-energy',
              'powerlfp','worldpower','taico','lansine','sinorise',
              'calife','factory','manufacturer','supplier','battery',
              'power station','solar','inverter','order','payment',
              'alibaba','led','lighting','certificate','ce ','fcc ',
              'un38.3','rohs','tracking','shipment']
        is_supplier = any(k in text for k in kw)
        has_price = bool(re.search(r'\$\s*\d+\.?\d*|\d+\s*usd', text, re.I))
        
        if is_supplier or has_price:
            results.append({'from': from_[:80], 'subject': subj[:120], 'date': date_,
                          'price': '💰' if has_price else '', 'supplier': '✅' if is_supplier else '⚠️'})
    
    mail.logout()
    
    print(json.dumps(results, ensure_ascii=False, indent=2))
    sys.stderr.write(f"\nSupplier emails found: {len(results)}\n")
    
except Exception as e:
    sys.stderr.write(f"ERROR: {e}\n{traceback.format_exc()}\n")
    sys.exit(1)
