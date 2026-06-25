#!/usr/bin/env python
"""Send 3 bullets: EGreen Egypt, ZNC Solar Pakistan, Capslock Thailand"""

import json, smtplib
from email.mime.text import MIMEText

env_path = r'C:\nichenexusglobal\.env'
password = None
with open(env_path, 'r') as fh:
    for raw in fh:
        raw = raw.strip()
        if raw.startswith('NICHE_EMAIL_PASSWORD'):
            password = raw.split('=', 1)[1].strip().strip("'\\\"")
            break
if not password:
    print("FAIL: password")
    exit(1)

smtp_host = "smtp.exmail.qq.com"
smtp_port = 465
sender = "pen@nichenexusglobal.com"

emails = [
    ("EGreen Egypt", "sales@egreen-eg.com",
     "LiFePO4 portable power stations - complementary line for your solar portfolio",
     "Hi EGreen team,\n\nI saw you're the official SOFAR distributor in Egypt, providing solar energy systems design, supply and installation across Cairo and Alexandria.\n\nWe're a sourcing company in Shenzhen, China, working with partner factories that produce LiFePO4 portable power stations. For your residential and commercial customers, portable power stations could be a practical add-on alongside your SOFAR inverters and battery storage.\n\nOur wholesale pricing reference:\n- 1024Wh/1000W ~ $145 FOB\n- 1280Wh/1200W ~ $205 FOB\n- 2048Wh/2400W ~ $298 FOB\n\nAll CE/FCC certified. OEM/private label available.\n\nIf this fits your product range, I can share spec sheets and more details.\n\nBest regards,\nPen\nnichenexusglobal.com"),
    ("ZNC Solar Pakistan", "sales@zncsolar.com",
     "LiFePO4 portable power stations - a natural extension for your battery portfolio",
     "Hi ZNC Solar team,\n\nI see you're the authorized GoodWe and Soluna distributor in Pakistan, a business built since 1991 with nationwide coverage.\n\nWe're a sourcing company in Shenzhen, China, working with partner factories that produce LiFePO4 portable power stations. For your distribution network that already handles Soluna batteries, adding portable power stations could be a natural complement.\n\nOur wholesale pricing reference:\n- 1024Wh/1000W ~ $145 FOB\n- 1280Wh/1200W ~ $205 FOB\n- 2048Wh/2400W ~ $298 FOB\n\nAll CE/FCC certified. OEM/private label available.\n\nIf this fits your product range, I can share spec sheets and more details.\n\nBest regards,\nPen\nnichenexusglobal.com"),
    ("Capslock Thailand", "info@capslockthai.com",
     "LiFePO4 portable power stations - a complementary brand for your lineup",
     "Hi Capslock team,\n\nI see you're the official Jackery distributor in Thailand, selling Explorer 1000 Pro and other models.\n\nWe're a sourcing company in Shenzhen, China, working with partner factories that produce LiFePO4 portable power stations. Having a complementary brand alongside Jackery could give your customers more options at different price points.\n\nOur wholesale pricing reference:\n- 1024Wh/1000W ~ $145 FOB\n- 1280Wh/1200W ~ $205 FOB\n- 2048Wh/2400W ~ $298 FOB\n\nAll CE/FCC certified. OEM/private label available.\n\nIf you're interested, I can send spec sheets and more details.\n\nBest regards,\nPen\nnichenexusglobal.com")
]

results = []
for company, recipient, subject, body in emails:
    msg = MIMEText(body)
    msg["From"] = f"Pen | nichenexusglobal <{sender}>"
    msg["To"] = recipient
    msg["Subject"] = subject
    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as server:
            server.login(sender, password)
            server.sendmail(sender, [recipient], msg.as_string())
        results.append(f"OK: {company} -> {recipient}")
    except Exception as e:
        results.append(f"FAIL: {company} -> {e}")
    print(f"  Sent {company}")

for r in results:
    print(r)

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)
companies = {"EGreen (Egyptian Renewable Energy Co.)": True, "ZNC Solar (Zahid & Co.)": True, "Capslock Co. Ltd (ThailandUPS)": True}
for b in db['email_bullets']:
    if b.get('company') in companies:
        b['sent'] = True
        b['sent_date'] = '2026-06-25'
        b['sent_channel'] = 'email'
        b['status'] = 'sent'
with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)
print("DB updated.")
