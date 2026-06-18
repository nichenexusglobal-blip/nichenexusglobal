#!/usr/bin/env python3
"""New supplier RFQs - June 5, second batch. Each personalized, each through the gate."""
import sys, os, time, json, smtplib, ssl
from email.mime.text import MIMEText

# Add gate to path
sys.path.insert(0, os.path.expanduser('~/nichenexusglobal'))
from supplier_rfq_gate import gate_check

SMTP_HOST = 'smtp.exmail.qq.com'
SMTP_PORT = 587
USER = 'pen@nichenexusglobal.com'
PASS = os.environ.get('NICHE_EMAIL_PASSWORD', '')

s = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
ctx = ssl.create_default_context()
s.starttls(context=ctx)
s.login(USER, PASS)

results = []

# ====== 1. Meco Power ======
# Products from Made-in-China: 300Wh ($62-68), 1000Wh ($138-168), 2000Wh ($288-300), 3000Wh/3.6kWh ($485-550)
# MOQ = 10, Shenzhen based
body1 = '''Hi Team,

I visited your website (mecopower.com) and saw your full portable power station range — from the 300Wh model (~$62-68 FOB) up to the 3.6kWh/3000W unit (~$485-550 FOB). Your pricing across the range is very competitive.

We have specific client requests right now:
- 300Wh class (300W output) for Philippine retailers — qty 50-100 pcs/month
- 1000Wh class for Middle East distributors — qty 30-50 pcs/month
- 2000Wh LiFePO4 for African buyers — qty 20-30 pcs/month

Could you confirm FOB Shenzhen unit pricing at MOQ 10 and at 50 pcs for these three models? Also, do they come with CE, RoHS, and UN38.3 certification?

Best regards,
Pen
nichenexusglobal.com'''

r1 = gate_check('Meco Power', body1, ['300Wh', '1000Wh', '2000Wh', '3600Wh'])
results.append(('Meco Power', 'sales@mecopower.com', r1))
if r1['passed']:
    msg = MIMEText(body1, 'plain', 'utf-8')
    msg['From'] = USER; msg['To'] = 'sales@mecopower.com'
    msg['Subject'] = 'RFQ: 300Wh / 1000Wh / 2000Wh LiFePO4 Portable Power Station'
    s.send_message(msg)
    print('[1/4] Meco Power — SENT')
time.sleep(2)

# ====== 2. LiPower Group ======
# M3000: 3000W, 2880Wh LiFePO4, MOQ=1, CE/ISO
body2 = '''Hi Team,

I saw your M3000 portable power station on lipowergroup.com — 3000W, 2880Wh LiFePO4 with MOQ=1, which is very attractive for our distributor clients who want to test before committing to container orders.

We have a South African distributor interested in 3000W-class units. Could you quote FOB Shenzhen for:
- 1 pc (sample)
- 10 pcs (trial)
- 50 pcs (bulk)

Does the M3000 come in 220-240V / 50Hz configuration? What certifications (CE, FCC, RoHS)?

Best regards,
Pen
nichenexusglobal.com'''

r2 = gate_check('LiPower Group', body2, ['M3000'])
results.append(('LiPower Group', 'marketing@lipowergroup.com', r2))
if r2['passed']:
    msg = MIMEText(body2, 'plain', 'utf-8')
    msg['From'] = USER; msg['To'] = 'marketing@lipowergroup.com'
    msg['Subject'] = 'RFQ: M3000 3000W LiFePO4 Portable Power Station'
    s.send_message(msg)
    print('[2/4] LiPower Group — SENT')
time.sleep(2)

# ====== 3. Bloo Power ======
# 17 years, 200Wh-5000Wh range, Shenzhen, 90,000+ customers
body3 = '''Hi Team,

I visited bloopower.com and saw your broad product range from 288Wh portable stations up to 5000Wh systems. 17 years in batteries is a strong track record.

We're sourcing for multiple markets in SE Asia and Africa. Specifically interested in:
- 288Wh / 300W LiFePO4 model (small retail market)
- 1000Wh / 1000W LiFePO4 model (home backup)
- 3600W large capacity model (for our SA distributor)

Could you share your product catalog with FOB Shenzhen pricing? Also, what certifications do your portable stations carry?

Best regards,
Pen
nichenexusglobal.com'''

r3 = gate_check('Bloo Power', body3, ['288Wh', '3600W'])
results.append(('Bloo Power', 'info@bloopower.com', r3))
if r3['passed']:
    msg = MIMEText(body3, 'plain', 'utf-8')
    msg['From'] = USER; msg['To'] = 'info@bloopower.com'
    msg['Subject'] = 'RFQ: 300W / 1000W / 3600W LiFePO4 Portable Power Station'
    s.send_message(msg)
    print('[3/4] Bloo Power — SENT')
time.sleep(2)

# ====== 4. Topure Power ======
# Founded 2011, CP3000/CP3600, clients include China Mobile/Unicom/State Grid
body4 = '''Hi Team,

I saw your CP3000 and CP3600 portable power stations on topurepower.com. Your client list including China Mobile and State Grid speaks to your reliability.

We need a 3000W-class LiFePO4 station for an African distributor. Could you quote FOB Shenzhen for the CP3000/CP3600 at:
- 5 pcs (trial)
- 20 pcs (first order)

Do these models come with 220-240V/50Hz output? What certifications do you hold?

Best regards,
Pen
nichenexusglobal.com'''

r4 = gate_check('Topure Power', body4, ['CP3000', 'CP3600'])
results.append(('Topure Power', 'sales@topurepower.com', r4))
if r4['passed']:
    msg = MIMEText(body4, 'plain', 'utf-8')
    msg['From'] = USER; msg['To'] = 'sales@topurepower.com'
    msg['Subject'] = 'RFQ: CP3000 / CP3600 LiFePO4 Portable Power Station'
    s.send_message(msg)
    print('[4/4] Topure Power — SENT')

s.quit()
print()

# Summary
print('=== RESULTS ===')
passed = 0
blocked = 0
for name, email, r in results:
    status = 'PASSED' if r['passed'] else f'BLOCKED ({r["score"]}/100)'
    if r['passed']: passed += 1
    else: blocked += 1
    print(f'{name:20s} | {email:30s} | Score: {r["score"]:3d}/100 | {status}')

print(f'\n{passed} sent, {blocked} blocked')

# Log
log_path = os.path.expanduser('~/nichenexusglobal/send_log.jsonl')
ts = time.strftime('%Y-%m-%dT%H:%M:%S+08:00')
with open(log_path, 'a') as f:
    for name, email, r in results:
        if r['passed']:
            f.write(json.dumps({'timestamp': ts, 'company': name, 'email': email, 'category': 'vendor_rfq', 'gate_score': r['score'], 'success': True}, ensure_ascii=False) + '\n')
