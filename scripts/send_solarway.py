#!/usr/bin/env python
"""Send email to Solarway Suppliers (SA) who asked us to email"""

import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

env_path = r'C:\nichenexusglobal\.env'
password = None
with open(env_path, 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith('NICHE_EMAIL_PASSWORD='):
            password = line.split('=', 1)[1].strip().strip("'\"")
            break

if not password:
    print("FAIL")
    exit(1)

smtp_host = "smtp.exmail.qq.com"
smtp_port = 465
sender = "pen@nichenexusglobal.com"
recipient = "info@solarwaysuppliers.co.za"

msg = MIMEMultipart("alternative")
msg["From"] = f"Pen | nichenexusglobal <{sender}>"
msg["To"] = recipient
msg["Subject"] = "LiFePO4 portable power stations – factory pricing"

text_body = """Hi Solarway Suppliers,

Pen here — we spoke on WhatsApp a few weeks ago and you asked me to send over some info via email. Apologies for the delay.

We're a sourcing company in Shenzhen, China, working with partner factories that produce LiFePO4 portable power stations. No middlemen, direct factory pricing.

Our range:
- 1024Wh/1000W ~ from $145 FOB
- 1280Wh/1200W ~ from $205 FOB
- 2048Wh/2400W ~ from $298 FOB

CE/FCC certified. MOQ from 10 units. OEM branding available.

If you're interested in adding portable power stations to your solar product range, I can send detailed specs and pricing.

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
