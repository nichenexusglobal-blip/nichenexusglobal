#!/usr/bin/env python
"""Send first-contact email to Iseli Energy (South Africa)"""

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
    print("FAIL: NICHE_EMAIL_PASSWORD not found")
    exit(1)

smtp_host = "smtp.exmail.qq.com"
smtp_port = 465
sender = "pen@nichenexusglobal.com"
recipient = "sales@iseli-energy.com"

msg = MIMEMultipart("alternative")
msg["From"] = f"Pen | nichenexusglobal <{sender}>"
msg["To"] = recipient
msg["Subject"] = "LiFePO4 portable power stations – a new line for your installer customers"

text_body = """Hi Iseli Energy team,

I see you're a solar wholesaler and system integrator in Cape Town serving residential, C&I and off-grid markets across Southern Africa. You supply solar professionals with brands like Huawei and Chint.

We're a sourcing company in Shenzhen, China, working with partner factories that produce LiFePO4 portable power stations. For your installer customers, portable power stations could be a natural upsell — a quick backup solution for homeowners who don't need a full system install.

Our wholesale pricing reference:
- 1024Wh/1000W ~ $145 FOB
- 1280Wh/1200W ~ $205 FOB
- 2048Wh/2400W ~ $298 FOB

All CE/FCC certified. OEM/private label available.

If this fits your product range, I can send spec sheets and more details.

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
