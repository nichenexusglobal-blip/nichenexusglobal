#!/usr/bin/env python3
"""Full inbox scan - read every email body, extract supplier info"""
import imaplib, email, json, sys, re, os
from email.header import decode_header

USER = 'pen@nichenexusglobal.com'
PASS = '4cd7vQ4GV59ATxxt'

OUTPUT = '/c/nichenexusglobal/inbox_data.jsonl'

SUPPLIER_DOMS = ['pecron.com','anern.com','califepower.com','bloopower.com',
                 'mecopower.com','shunxiangenergy.com','ie-energy.com',
                 'powerlfp.com','wpbattery.com','piforz.com','taicopower.com',
                 'lansinestorage.com','namkoo-power.com','adfbattery.com',
                 'iforway.com','cxjpowers.com','safecloudpower.com',
                 'houny.cn','bicodi.com','topurepower.com','onesunpv.com',
                 'spowerstation.com','tursan-energy.com','mustenergy.com',
                 'meindchina.com','oukitel.com','fjhuari.com']
                 
SUPPLIER_KWS = ['fob','exw','moq','quote','quotation','catalog','catalogue',
                'price','pricing','sample','shipping','delivery','lead time',
                'oem','cert','ce ','fcc','un38.3','rohs','payment',
                'proforma','invoice','pi ','order','factory','manufacturer',
                'battery','power station','solar','inverter']

def is_supplier_email(from_addr, subj, body):
    """Check if this is a meaningful supplier communication"""
    text = (from_addr + ' ' + subj + ' ' + body[:300]).lower()
    # Must be from a supplier domain or contain supplier keywords in reply
    has_domain = any(dom in from_addr.lower() for dom in SUPPLIER_DOMS)
    has_kw = any(kw in text for kw in SUPPLIER_KWS)
    
    # Skip system emails
    if 'hermes agent' in subj.lower() or 'cronjob' in subj.lower():
        return False
    if '退信' in subj or 'undeliverable' in subj.lower() or 'delivery status' in subj.lower():
        return False
    
    return has_domain or (has_kw and ('re:' in subj.lower() or '回复' in subj))

try:
    mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993, timeout=30)
    mail.login(USER, PASS)
    
    total_found = 0
    for folder in ['INBOX', '"Sent Messages"']:
        try:
            mail.select(folder)
        except:
            continue
        
        status, data = mail.search(None, 'ALL')
        mids = data[0].split() if data[0] else []
        sys.stderr.write(f"{folder}: {len(mids)} messages\n")
        
        batch_size = 50
        for batch_start in range(0, len(mids), batch_size):
            batch = mids[batch_start:batch_start+batch_size]
            
            for mid in batch:
                status, d = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
                if status != 'OK' or not d or not d[0]: continue
                
                try:
                    raw = d[0][1]
                    if isinstance(raw, bytes):
                        hdr = raw.decode('utf-8', errors='replace')
                    else:
                        continue
                except:
                    continue
                
                # Extract From
                from_ = ''
                for line in hdr.split('\n'):
                    if line.startswith('From:'):
                        from_ = line[5:].strip()
                        break
                
                # Extract Subject
                subj_raw = ''
                for line in hdr.split('\n'):
                    if line.startswith('Subject:'):
                        subj_raw = line[8:].strip()
                        break
                
                # Decode subject
                if '=?' in subj_raw:
                    try:
                        sp = decode_header(subj_raw)
                        subj = ''
                        for p, c in sp:
                            if isinstance(p, bytes):
                                subj += p.decode(c or 'utf-8', errors='replace')
                            else:
                                subj += str(p)
                    except:
                        subj = subj_raw
                else:
                    subj = subj_raw
                
                # Quick filter
                if ('hermes agent' in subj.lower() or 'cronjob' in subj.lower() or 
                    'harness' in subj.lower()):
                    continue
                
                if not any(dom in from_.lower() for dom in SUPPLIER_DOMS):
                    continue
                
                # Get full body
                status2, d2 = mail.fetch(mid, '(RFC822)')
                if status2 != 'OK' or not d2 or not d2[0]: continue
                try:
                    msg = email.message_from_bytes(d2[0][1])
                except:
                    continue
                
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
                
                date_ = str(msg['Date'] or '?')
                
                # Clean body - remove quoted text
                lines = body.split('\n')
                clean = []
                for line in lines:
                    s = line.strip()
                    if s.startswith('>') or 'Original Message' in s or '---Original---' in s:
                        break
                    if s.startswith('From:') or s.startswith('Sent:') or s.startswith('Date:'):
                        continue
                    if s.startswith('To:') or s.startswith('Subject:'):
                        continue
                    clean.append(line)
                body_clean = '\n'.join(clean).strip()
                
                total_found += 1
                entry = {
                    'folder': folder,
                    'from': from_[:80],
                    'subject': subj[:150],
                    'date': date_,
                    'body': body_clean[:2000]
                }
                
                # Append to output file
                with open(OUTPUT, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                
                sys.stderr.write(f"[{total_found}] {folder} | {from_[:50]} | {subj[:60]}\n")
    
    mail.logout()
    print(f"\nTotal supplier emails saved to {OUTPUT}: {total_found}", file=sys.stderr)

except Exception as e:
    sys.stderr.write(f"ERROR: {e}\n")
    sys.exit(1)
