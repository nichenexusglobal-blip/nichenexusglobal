"""
Batch 2: New Africa/Middle East nails for portable power station.
"""
import smtplib, ssl, time
from email.mime.text import MIMEText

EMAIL = "pen@nichenexusglobal.com"
PASSWORD = "mE...HOST = "smtp.exmail.qq.com"
SMTP_PORT = 465

targets = [
    ("sales@siwsa.co.za", "Inverter Warehouse SA", "Africa",
     "SA solar inverter retailer — natural fit for portable power stations"),
    ("sales@communica.co.za", "Communica SA", "Africa",
     "SA electronics and industrial supplier"),
    ("sales@matrixwarehouse.co.za", "Matrix Warehouse SA", "Africa",
     "SA electronics and computer retailer"),
    ("customercare@dubairetail.ae", "Dragon Mart Dubai", "ME",
     "Dubai's largest Chinese goods trading hub"),
]

body_africa = """I'm reaching out from nichenexusglobal, a cross-border trade connector based in China.

We help solar and electronics retailers source portable power stations directly from verified OEM factories — with factory verification, pricing negotiation, quality inspection, and logistics support.

Current verified factory pricing (LiFePO4 battery, pure sine wave inverter):

600W class (299-576Wh):
- ALLPOWERS R600: $150/unit factory price
- Pecron E500LFP: $130/unit (CE/FCC/UKCA certified, 2-year warranty)
- PiForz PF500: available on request (UL/CE/FCC certified)

1000W class (1056-1210Wh):
- Pecron E1000LFP: $240/unit
- ALLPOWERS R1500 LITE: $300/unit
- PiForz PF1500: available on request

2500W class (2016Wh):
- ALLPOWERS R2500: $430/unit

Minimum order 50-100 units per model. 7-35 day production.

South Africa faces ongoing load shedding — portable power stations are a growing category. We can help you add a competitively priced line to your product range.

Are you currently sourcing portable power stations? Happy to discuss.

Pen
nichenexusglobal.com"""

body_me = body_africa.replace(
    "South Africa faces ongoing load shedding — portable power stations are a growing category. We can help you add a competitively priced line to your product range.",
    "The Middle East has strong demand for portable power — from outdoor recreation to backup power for homes and businesses. We can help you add a competitively priced line to your product range."
)

subject = "Portable Power Stations: 3-Factory Price Comparison (600W-2500W)"

context = ssl.create_default_context()
sent = 0

print(f"Sending to {len(targets)} targets...\n")

for target_email, company, region, desc in targets:
    body = body_me if region == "ME" else body_africa
    
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["From"] = f"Pen <{EMAIL}>"
        msg["To"] = target_email
        msg["Subject"] = subject
        
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as s:
            s.ehlo()
            s.login(EMAIL, PASSWORD)
            s.sendmail(EMAIL, [target_email], msg.as_string())
        
        print(f"  SENT: {target_email} ({company}) - {desc}")
        sent += 1
        time.sleep(8)
        
    except Exception as e:
        print(f"  FAIL: {target_email}: {str(e)[:150]}")
        time.sleep(3)

print(f"\nDONE: {sent}/{len(targets)} sent")
