#!/usr/bin/env python3
"""Send follow-up email to KWT Tech Mart"""
import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.exmail.qq.com"
SMTP_PORT = 465
FROM = "pen@nichenexusglobal.com"
PASSWORD = "4cd7vQ4GV59ATxxt"
TO = "sales@kwttechmart.com"

body = """Hi KWT Tech Mart team,

Following up on our WhatsApp conversation — here's the product info you asked for.

1280Wh LiFePO4 Portable Power Station
- Capacity: 1280Wh (LiFePO4 battery)
- Output: 1200W pure sine wave AC
- Charging: AC / Solar (MPPT) / Car
- Socket: UK plug (Type G), 220-240V
- Certification: CE, FCC
- Weight: 18kg
- Price: $205 FOB Shenzhen
- MOQ: 10 units

I can also send you product photos and a spec sheet PDF if you're interested.

Best regards,
Pen
www.nichenexusglobal.com"""

msg = MIMEText(body, "plain", "utf-8")
msg["Subject"] = "Portable power station 1280Wh LiFePO4 — following up on our WhatsApp chat"
msg["From"] = FROM
msg["To"] = TO

try:
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=20) as s:
        s.login(FROM, PASSWORD)
        s.send_message(msg)
    print(f"✅ Sent to {TO}")
except Exception as e:
    print(f"❌ Failed: {e}")
