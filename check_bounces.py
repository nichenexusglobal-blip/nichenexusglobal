import imaplib, ssl, email, re
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta, timezone

TZ8 = timezone(timedelta(hours=8))
PWD = 'mE3REReV7RmjDRZT'

def ds(s):
    if not s: return ''
    parts = decode_header(s)
    r = []
    for p, c in parts:
        if isinstance(p, bytes):
            try: r.append(p.decode(c or 'utf-8', errors='replace'))
            except: r.append(p.decode('utf-8', errors='replace'))
        else: r.append(str(p))
    return ''.join(r)

def get_dt(msg):
    try: return parsedate_to_datetime(ds(msg['Date'])).astimezone(TZ8)
    except: return None

ctx = ssl.create_default_context()
mail = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993, ssl_context=ctx)
mail.login('pen@nichenexusglobal.com', PWD)
mail.select('INBOX')
status, data = mail.search(None, 'ALL')
all_ids = data[0].split()
print(f'INBOX total: {len(all_ids)}')

bounce_kw = ['undeliver', 'returned', 'bounce', 'failure', 'delivery status', 
             'mail delivery', 'postmaster', 'mailer-daemon', '550', '5.1.1', 
             'does not exist', 'user unknown']

bounces = []
for mid in all_ids:
    status, md = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (DATE FROM SUBJECT)])')
    if status != 'OK': continue
    raw = md[0][1]
    msg = email.message_from_bytes(raw)
    dt = get_dt(msg)
    if not dt: continue
    frm = ds(msg['From']).lower()
    subj = ds(msg['Subject']).lower()
    
    combined = frm + ' ' + subj
    if any(kw in combined for kw in bounce_kw):
        bounces.append({
            'mid': mid.decode(), 
            'from': ds(msg['From'])[:80], 
            'subj': ds(msg['Subject'])[:120], 
            'date': dt.strftime('%Y-%m-%d %H:%M')
        })

print(f'Bounce indicators found: {len(bounces)}')

# Fetch full body of last 10 bounces
for b in bounces[-10:]:
    status, md = mail.fetch(b['mid'].encode(), '(RFC822)')
    if status != 'OK': continue
    msg = email.message_from_bytes(md[0][1])
    body = ''
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get('Content-Disposition', ''))
            if ct in ('text/plain','text/html') and 'attachment' not in cd:
                try:
                    bb = part.get_payload(decode=True)
                    if bb: 
                        body += bb.decode(part.get_content_charset() or 'utf-8', errors='replace') + '\n'
                except: pass
    else:
        try:
            bb = msg.get_payload(decode=True)
            if bb: body = bb.decode(msg.get_get_content_charset() or 'utf-8', errors='replace')
        except: pass
    
    failed = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', body)
    failed_unique = [e for e in set(failed) if 'nichenexusglobal' not in e.lower()]
    
    print(f'\n[{b["date"]}] {b["from"][:60]}')
    print(f'  Failed recipients: {failed_unique[:5]}')
    
    for line in body.split('\n'):
        line_stripped = line.strip()
        low = line_stripped.lower()
        if any(kw in low for kw in ['550','551','552','553','554','5.1.1','5.4.1',
                                       'undeliver','user unknown','does not exist','rejected',
                                       'mailbox','no such']):
            print(f'  > {line_stripped[:250]}')

mail.close()
mail.logout()
