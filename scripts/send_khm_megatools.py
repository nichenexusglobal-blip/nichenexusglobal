#!/usr/bin/env python
"""Send first-contact email to KHM Megatools Corp. (Philippines)"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Read password from .env
env_path = r'C:\nichenexusglobal\.env'
password = None
with open(env_path, 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith('NICHE_EMAIL_PASSWORD='):
            password = line.split('=', 1)[1].strip().strip("'\"")
            break

if not password:
    print("FAIL: EMAIL_PASSWORD not found in .env")
    exit(1)

# Email config
smtp_host = "smtp.exmail.qq.com"
smtp_port = 465
sender = "pen@nichenexusglobal.com"
recipient = "sales@khmtools.com.ph"

# Build email
msg = MIMEMultipart("alternative")
msg["From"] = f"Pen | nichenexusglobal <{sender}>"
msg["To"] = recipient
msg["Subject"] = "LiFePO4 power stations – complement your portable generator lineup"

# Plain text version
text_body = """Hi KHM team,

I was looking at your power station range at khmtools.com.ph and noticed you carry Yamato, Greenfield, Daiden and Wadfow models from 200W to 800W.

We're a sourcing company based in Shenzhen, China, working with partner factories that produce LiFePO4 portable power stations. Your current lineup stops at 800W (Yamato YM63-800 at ₱19,500) and uses Li-Ion batteries in the Daiden series.

LiFePO4 offers significantly more cycle life (6000+ vs 500-800 cycles) and better thermal stability. For reference, our typical wholesale pricing:

• 1024Wh/1000W ~ $145 FOB
• 1280Wh/1200W ~ $205 FOB
• 2048Wh/2400W ~ $298 FOB

If you're interested in adding LiFePO4 models or higher-capacity units (1000W+) to your product range, I'd be happy to send spec sheets and a formal quotation.

Best regards,
Pen
nichenexusglobal.com"""

# HTML version
html_body = """<html><body style="font-family: Arial, sans-serif; color: #333;">
<p>Hi KHM team,</p>
<p>I was looking at your power station range at <a href="https://khmtools.com.ph/collections/power-station">khmtools.com.ph</a> and noticed you carry Yamato, Greenfield, Daiden and Wadfow models from 200W to 800W.</p>
<p>We're a sourcing company based in Shenzhen, China, working with partner factories that produce LiFePO4 portable power stations. Your current lineup stops at 800W (Yamato YM63-800 at ₱19,500) and uses Li-Ion batteries in the Daiden series.</p>
<p>LiFePO4 offers significantly more cycle life (6000+ vs 500-800 cycles) and better thermal stability. For reference, our typical wholesale pricing:</p>
<table style="border-collapse: collapse; width: 100%; max-width: 400px;">
<tr style="background: #f5f5f5;"><td style="padding: 8px; border: 1px solid #ddd;">1024Wh/1000W</td><td style="padding: 8px; border: 1px solid #ddd;">~$145 FOB</td></tr>
<tr><td style="padding: 8px; border: 1px solid #ddd;">1280Wh/1200W</td><td style="padding: 8px; border: 1px solid #ddd;">~$205 FOB</td></tr>
<tr style="background: #f5f5f5;"><td style="padding: 8px; border: 1px solid #ddd;">2048Wh/2400W</td><td style="padding: 8px; border: 1px solid #ddd;">~$298 FOB</td></tr>
</table>
<br>
<p>If you're interested in adding LiFePO4 models or higher-capacity units (1000W+) to your product range, I'd be happy to send spec sheets and a formal quotation.</p>
<br>
<p>Best regards,<br>Pen<br><a href="https://nichenexusglobal.com">nichenexusglobal.com</a></p>
</body></html>"""

msg.attach(MIMEText(text_body, "plain"))
msg.attach(MIMEText(html_body, "html"))

# Send
try:
    with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as server:
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())
    print(f"SUCCESS: Email sent to {recipient}")
except Exception as e:
    print(f"FAIL: {e}")
    exit(1)
