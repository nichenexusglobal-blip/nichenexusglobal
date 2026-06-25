#!/usr/bin/env python
"""Send first-contact email to Prime Tech Trading (Philippines)"""

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
recipient = "sales@primetechtrading.ph"

msg = MIMEMultipart("alternative")
msg["From"] = f"Pen | nichenexusglobal <{sender}>"
msg["To"] = recipient
msg["Subject"] = "LiFePO4 power stations – a complementary line for your distribution network"

text_body = """Hi Prime Tech team,

I saw your company's page at primetechtrading.ph — you distribute BLUETTI and Anker SOLIX across the Philippines, Luzon to Mindanao. That's a solid distribution network you've built.

We're a sourcing company in Shenzhen, China, working with partner factories that produce LiFePO4 portable power stations. Your lineup covers the premium tier (BLUETTI AC series, Anker SOLIX), and we could be a source for a mid-range option to complement those brands.

For reference, our wholesale pricing:
- 1024Wh/1000W ~ $145 FOB
- 1280Wh/1200W ~ $205 FOB
- 2048Wh/2400W ~ $298 FOB

All CE/FCC certified. Private label/OEM available if you're interested in building your own brand.

Would you like me to send spec sheets and a catalog of the full range?

Best regards,
Pen
nichenexusglobal.com"""

html_body = """<html><body style="font-family: Arial, sans-serif; color: #333;">
<p>Hi Prime Tech team,</p>
<p>I saw your company's page at <a href="https://primetechtrading.ph">primetechtrading.ph</a> — you distribute BLUETTI and Anker SOLIX across the Philippines, Luzon to Mindanao. That's a solid distribution network you've built.</p>
<p>We're a sourcing company in Shenzhen, China, working with partner factories that produce LiFePO4 portable power stations. Your lineup covers the premium tier (BLUETTI AC series, Anker SOLIX), and we could be a source for a mid-range option to complement those brands.</p>
<p>For reference, our wholesale pricing:</p>
<table style="border-collapse:collapse;width:100%;max-width:400px;">
<tr style="background:#f5f5f5;"><td style="padding:8px;border:1px solid #ddd;">1024Wh/1000W</td><td style="padding:8px;border:1px solid #ddd;">~$145 FOB</td></tr>
<tr><td style="padding:8px;border:1px solid #ddd;">1280Wh/1200W</td><td style="padding:8px;border:1px solid #ddd;">~$205 FOB</td></tr>
<tr style="background:#f5f5f5;"><td style="padding:8px;border:1px solid #ddd;">2048Wh/2400W</td><td style="padding:8px;border:1px solid #ddd;">~$298 FOB</td></tr>
</table>
<br>
<p>All CE/FCC certified. Private label/OEM available if you're interested in building your own brand.</p>
<p>Would you like me to send spec sheets and a catalog of the full range?</p>
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
