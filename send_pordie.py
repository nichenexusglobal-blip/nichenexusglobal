#!/usr/bin/env python3
"""Send inquiry to SOUOP/Pordie Energy"""
import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.exmail.qq.com"
SMTP_PORT = 465
FROM = "pen@nichenexusglobal.com"
PASSWORD = "4cd7vQ4GV59ATxxt"
TO = "info@souoppowerstation.com"

body = """Hi SOUOP team,

I'm reaching out from China. We're building supply options for African importers and came across your SOUOP lineup.

Could you share your catalog and FOB pricing?

Best regards,
Pen
www.nichenexusglobal.com"""

msg = MIMEText(body, "plain", "utf-8")
msg["Subject"] = "Inquiry: LiFePO4 portable power station catalog & pricing"
msg["From"] = FROM
msg["To"] = TO

try:
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=20) as s:
        s.login(FROM, PASSWORD)
        s.send_message(msg)
    print(f"✅ Sent to {TO}")
except Exception as e:
    print(f"❌ Failed: {e}")
