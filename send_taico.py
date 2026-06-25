#!/usr/bin/env python3
"""Send follow-up email to Taico Technology (Kelly)"""
import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.exmail.qq.com"
SMTP_PORT = 465
FROM = "pen@nichenexusglobal.com"
PASSWORD = "4cd7vQ4GV59ATxxt"
TO = "sales20@taicopower.com"

body = """Hi Kelly,

Following up on the TKPW specs you shared. We're building supply options for clients in Africa and Southeast Asia, and your series fits their needs well. We'd like to start with two models:
- TKPW-A1000 (1004.8Wh/300W)
- TKPW-A1000 Pro (1004.8Wh/500W)

Could you share FOB pricing and estimated lead time at MOQ 200?

Looking forward to your quote.

Best regards,
Pen
www.nichenexusglobal.com"""

msg = MIMEText(body, "plain", "utf-8")
msg["Subject"] = "Re: Inquiry: 1000W LiFePO4 Portable Power Station OEM — 200-500 units"
msg["From"] = FROM
msg["To"] = TO

try:
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=20) as s:
        s.login(FROM, PASSWORD)
        s.send_message(msg)
    print(f"✅ Sent to {TO}")
except Exception as e:
    print(f"❌ Failed: {e}")
