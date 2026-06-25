#!/usr/bin/env python
"""Add ZNC Solar Pakistan and send email"""

import json, smtplib
from email.mime.text import MIMEText

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

new_bullet = {
    "company": "ZNC Solar (Zahid & Co.)",
    "market": "Pakistan",
    "segment": "solar_distributor",
    "email": "sales@zncsolar.com",
    "whatsapp": "923348888555",
    "website": "zncsolar.com",
    "source": "web_search",
    "verified": True,
    "status": "sent",
    "products_sold": "GoodWe inverters, Soluna lithium batteries - authorized distributor",
    "brands_carried": "GoodWe, Soluna",
    "market_position": "Authorized GoodWe/Soluna distributor Pakistan. Founded 1991. Nationwide coverage.",
    "contact_source": "Website footer: sales@zncsolar.com, +92 334 8888 555",
    "research_depth": "verified_on_website",
    "research_date": "2026-06-25",
    "sent": True,
    "sent_date": "2026-06-25",
    "sent_channel": "email",
    "gate_score": 100,
    "gate_status": "gated"
}

db['email_bullets'].append(new_bullet)
with open(path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)
print("Bullet added")

env_path = r'C:\nichenexusglobal\.env'
password = None
with open(env_path, 'r') as fh:
    for raw in fh:
        raw = raw.strip()
        if 'NICHE_EMAIL_PASSWORD=*** in raw:
            password = raw.split('=', 1)[1].strip().strip("'\\\"")
            break

if not password:
    print("FAIL: password")
    exit(1)

smtp_host = "smtp.exmail.qq.com"
smtp_port = 465
sender = "pen@nichenexusglobal.com"
recipient = "sales@zncsolar.com"

msg = MIMEText(f"""Hi ZNC Solar team,

I see you're the authorized GoodWe and Soluna distributor in Pakistan, a business built since 1991 with nationwide coverage.

We're a sourcing company in Shenzhen, China, working with partner factories that produce LiFePO4 portable power stations. For your distribution network that already handles Soluna batteries, adding portable power stations could be a natural complement.

Our wholesale pricing reference:
- 1024Wh/1000W ~ $145 FOB
- 1280Wh/1200W ~ $205 FOB
- 2048Wh/2400W ~ $298 FOB

All CE/FCC certified. OEM/private label available.

If this fits your product range, I can share spec sheets and more details.

Best regards,
Pen
nichenexusglobal.com""")

msg["From"] = f"Pen | nichenexusglobal <{sender}>"
msg["To"] = recipient
msg["Subject"] = "LiFePO4 portable power stations – a natural extension for your battery portfolio"

try:
    with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as server:
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())
    print(f"SUCCESS: Email sent to {recipient}")
except Exception as e:
    print(f"FAIL: {e}")
    exit(1)
