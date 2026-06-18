"""
Send portable power station outreach to NEW nails (Africa + LatAm).
"""
import smtplib, ssl, time
from email.mime.text import MIMEText

EMAIL = "pen@nichenexusglobal.com"
PASSWORD = "mE3REReV7RmjDRZT"
SMTP_HOST = "smtp.exmail.qq.com"
SMTP_PORT = 465

targets = [
    ("sales@thesunpays.co.za", "The Sun Pays", "Africa", 
     "South Africa's solar and inverter retailer"),
    ("info@thesunpays.co.za", "The Sun Pays", "Africa",
     "South Africa's solar and inverter retailer"),
    ("support@solar-shop.co.za", "Solar Shop SA", "Africa",
     "South Africa's solar equipment retailer"),
    ("info@sustainable.co.za", "Sustainable.co.za", "Africa",
     "South Africa's sustainable living retailer"),
    ("atencion@liverpool.com.mx", "Liverpool Mexico", "LatAm",
     "Mexico's largest department store — electronics, home, camping"),
]

body_africa = """I'm reaching out from nichenexusglobal, a cross-border trade connector based in China.

We help solar and energy retailers source portable power stations directly from verified OEM factories — with factory verification, pricing negotiation, quality inspection, and logistics support.

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

South Africa's load shedding creates strong demand for reliable backup power. We can help you build a competitively priced portable power station line for your customer base.

Are you currently sourcing portable power stations? Happy to discuss your requirements.

Pen
nichenexusglobal.com"""

body_latam = body_africa.replace(
    "South Africa's load shedding creates strong demand for reliable backup power. We can help you build a competitively priced portable power station line for your customer base.",
    "Mexico's outdoor recreation and emergency preparedness markets are growing rapidly. We can help you build a competitively priced portable power station line for your customer base."
)

subject = "Portable Power Stations: 3-Factory Price Comparison (600W-2500W)"

context = ssl.create_default_context()
sent = 0

print(f"Sending to {len(targets)} new targets...\n")

for target_email, company, region, desc in targets:
    body = body_latam if region == "LatAm" else body_africa
    
    # Slight variation for duplicate domain (thesunpays)
    if "thesunpays" in target_email and "info@" in target_email:
        body = body.replace("I'm reaching out from", "Following up on behalf of")
    
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
        print(f"  FAIL: {target_email} ({company}): {str(e)[:150]}")
        time.sleep(3)

print(f"\nDONE: {sent}/{len(targets)} sent")
