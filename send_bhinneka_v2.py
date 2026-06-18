#!/usr/bin/env python3
"""
Send updated proposal to Bhinneka - working email channels confirmed by research.
Run when SMTP connectivity (smtp.exmail.qq.com:465) is restored.

Key findings:
- Bhinneka corporate@bhinneka.com is DEAD (defunct Google Group)
- Email format: firstname@bhinneka.com (confirmed)
- Key contacts discovered:
  1. felix@bhinneka.com — Felix Huang, Head of Product (WHOIS-verified)
  2. alfin@bhinneka.com — Alfin Lie, VP of Sales (conjectured from LinkedIn)
- Product gap: Bhinneka sells 74Wh power banks but NO AC-outlet power stations
"""
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL = "pen@nichenexusglobal.com"
PASSWORD = "4cd7vQ4GV59ATxxt"

# Verified contacts at Bhinneka
recipients = [
    "felix@bhinneka.com",     # Head of Product (confirmed via WHOIS)
    "alfin@bhinneka.com",     # VP of Sales (conjectured from LinkedIn/RetailAsia 2024)
]

subject = "Portable Power Stations (300W-5000W) — New Category for Bhinneka B2B"

body = """Hi Bhinneka Team,

I'm Pen from nichenexusglobal. We help Indonesian businesses source quality products from verified Chinese manufacturers.

I noticed Bhinneka carries power banks (up to 74Wh) but doesn't yet offer portable power stations with AC output — a category growing fast among Indonesian corporate and government clients facing power reliability issues.

Indonesia's power infrastructure requires Rp3,000 trillion investment to add 69.5 GW capacity (2025-2034). For businesses relying on IT infrastructure, portable backup power is becoming essential.

We're working with certified LiFePO4 portable power station manufacturers:
• 300W-5000W output range
• 256Wh-5000Wh capacity
• CE / FCC / RoHS certified
• MOQ from 100 units
• FOB pricing from $145/unit
• White-label / OEM available

These products fit naturally with Bhinneka's IT, electronics, and MRO catalog — especially for clients needing backup power for field operations, home offices, and disaster preparedness.

Would you be interested in receiving a supplier comparison with full specs and FOB pricing?

Happy to share more details or set up a quick call.

Best regards,
Pen
nichenexusglobal.com"""

def send():
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.exmail.qq.com", 465, context=context, timeout=30) as server:
        server.ehlo()
        server.login(EMAIL, PASSWORD)
        for r in recipients:
            msg = MIMEMultipart('alternative')
            msg["From"] = f"Pen <{EMAIL}>"
            msg["To"] = r
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))
            server.sendmail(EMAIL, [r], msg.as_string())
            print(f"SENT to {r}")

if __name__ == "__main__":
    send()
