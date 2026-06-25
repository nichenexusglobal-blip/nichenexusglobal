#!/usr/bin/env python
"""Send first-contact email to Bluetti PH (bluettipower.ph)"""

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
recipient = "sale-ph@bluettipower.com"

msg = MIMEMultipart("alternative")
msg["From"] = f"Pen | nichenexusglobal <{sender}>"
msg["To"] = recipient
msg["Subject"] = "LiFePO4 power stations – complementary OEM line for PH dealers"

text_body = """Hi Bluetti PH team,

I see you're running bluettipower.ph — the official BLUETTI store for the Philippines with the Elite 30 V2, Elite 200 V2, and the full BLUETTI range. I also noticed you have a "Become a Dealer" program.

We're a sourcing company in Shenzhen, China, working with partner factories that produce LiFePO4 portable power stations. For your dealer network, having a complementary brand at a different price point alongside BLUETTI could be valuable.

For reference, our wholesale pricing:
- 1024Wh/1000W ~ $145 FOB
- 1280Wh/1200W ~ $205 FOB
- 2048Wh/2400W ~ $298 FOB

All CE/FCC certified. OEM/private label available.

If this is of interest to your dealer program, I can share spec sheets and more details.

Best regards,
Pen
nichenexusglobal.com"""

html_body = """<html><body style="font-family:Arial,sans-serif;color:#333;">
<p>Hi Bluetti PH team,</p>
<p>I see you're running <a href="https://bluettipower.ph">bluettipower.ph</a> — the official BLUETTI store for the Philippines with the Elite 30 V2, Elite 200 V2, and the full BLUETTI range. I also noticed you have a "Become a Dealer" program.</p>
<p>We're a sourcing company in Shenzhen, China, working with partner factories that produce LiFePO4 portable power stations. For your dealer network, having a complementary brand at a different price point alongside BLUETTI could be valuable.</p>
<p>For reference, our wholesale pricing:</p>
<table style="border-collapse:collapse;width:100%;max-width:400px;">
<tr style="background:#f5f5f5;"><td style="padding:8px;border:1px solid #ddd;">1024Wh/1000W</td><td style="padding:8px;border:1px solid #ddd;">~$145 FOB</td></tr>
<tr><td style="padding:8px;border:1px solid #ddd;">1280Wh/1200W</td><td style="padding:8px;border:1px solid #ddd;">~$205 FOB</td></tr>
<tr style="background:#f5f5f5;"><td style="padding:8px;border:1px solid #ddd;">2048Wh/2400W</td><td style="padding:8px;border:1px solid #ddd;">~$298 FOB</td></tr>
</table>
<br>
<p>All CE/FCC certified. OEM/private label available.</p>
<p>If this is of interest to your dealer program, I can share spec sheets and more details.</p>
<br>
<p>Best regards,<br>Pen<br><a href="https://nichenexusglobal.com">nichenexusglobal.com</a></p>
</body></html>"""

msg.attach(MIMEText(text_body, "plain"))
msg.attach(MIMEText(html_body, "html"))

try:
    with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as server:
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())
    print(f"SUCCESS: Email sent to {recipient}")
except Exception as e:
    print(f"FAIL: {e}")
    exit(1)
