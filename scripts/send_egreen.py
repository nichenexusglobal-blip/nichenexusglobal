#!/usr/bin/env python
"""Add EGreen Egypt as new bullet and send email"""

import json, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

# Add EGreen Egypt
new_bullet = {
    "company": "EGreen (Egyptian Renewable Energy Co.)",
    "market": "Egypt",
    "segment": "solar_distributor",
    "email": "sales@egreen-eg.com",
    "whatsapp": "201097770457",
    "website": "egreen-eg.com",
    "source": "web_search",
    "verified": True,
    "status": "sent",
    "products_sold": "SOFAR solar inverters, battery storage, solar water heaters - official SOFAR distributor Egypt",
    "brands_carried": "SOFAR",
    "market_position": "Official SOFAR distributor Egypt. Systems design, supply, installation. Cairo & Alexandria.",
    "contact_source": "Website: sales@egreen-eg.com, +2 010 9777 0457",
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
print("Bullet added to DB")

# Send email
env_path = r'C:\nichenexusglobal\.env'
password = None
with open(env_path, 'r') as fh:
    for raw in fh:
        raw = raw.strip()
        if 'NICHE_EMAIL_PASSWORD=' in raw:
            password = raw.split('=', 1)[1].strip().strip("'\\\"")
            break

if not password:
    print("FAIL: password not found")
    exit(1)

smtp_host = "smtp.exmail.qq.com"
smtp_port = 465
sender = "pen@nichenexusglobal.com"
recipient = "sales@egreen-eg.com"

msg = MIMEMultipart("alternative")
msg["From"] = f"Pen | nichenexusglobal <{sender}>"
msg["To"] = recipient
msg["Subject"] = "LiFePO4 portable power stations – complementary line for your solar portfolio"

text_body = """Hi EGreen team,

I saw you're the official SOFAR distributor in Egypt, providing solar energy systems design, supply and installation across Cairo and Alexandria.

We're a sourcing company in Shenzhen, China, working with partner factories that produce LiFePO4 portable power stations. For your residential and commercial customers, portable power stations could be a practical add-on alongside your SOFAR inverters and battery storage.

Our wholesale pricing reference:
- 1024Wh/1000W ~ $145 FOB
- 1280Wh/1200W ~ $205 FOB
- 2048Wh/2400W ~ $298 FOB

All CE/FCC certified. OEM/private label available.

If this fits your product range, I can share spec sheets and more details.

Best regards,
Pen
nichenexusglobal.com"""

msg.attach(MIMEText(text_body, "plain"))

try:
    with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as server:
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())
    print(f"SUCCESS: Email sent to {recipient}")
except Exception as e:
    print(f"FAIL: {e}")
    exit(1)
