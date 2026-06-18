"""
Send portable power station follow-up with comparison pricing.
Skip known bounces. Ignore IMAP false-positive reply detection.
"""
import smtplib, ssl, time
from email.mime.text import MIMEText

EMAIL = "pen@nichenexusglobal.com"
PASSWORD = "mE3REReV7RmjDRZT"
SMTP_HOST = "smtp.exmail.qq.com"
SMTP_PORT = 465

# All 18 targets; skip confirmed bounces
targets = [
    ("info@powernsun.com", "Power & Sun UAE"),
    ("dubai@ecosmart-intl.com", "EcoSmart International"),
    # help@solar-dubai.com - BOUNCED
    ("inquiries@solarphilippines.ph", "Solar Philippines"),
    ("sales@luminoussolar.com", "Luminous Solar"),
    ("customercare@su-kam.com", "Su-Kam India"),
    ("info@utl.co.in", "UTL India"),
    ("candra.hermawan@selis.co.id", "Selis Indonesia"),
    # customer.care@acehardware.co.id - BOUNCED
    # cs@electroniccity.co.id - BOUNCED
    # customer.service@homepro.co.th - BOUNCED
    # contact@advice.co.th - BOUNCED
    # info@jib.co.th - BOUNCED
    # hotro@fpt.com.vn - BOUNCED
    ("cskh@thegioididong.com", "Dien May Xanh Vietnam"),
    ("support@invertersupply.com", "Inverter Supply"),
    ("info@thesolarstore.com", "The Solar Store"),
    ("info@solarpanelstore.com", "Solar Panel Store"),
]

body_me = """I'm following up on our earlier message about portable power stations.

We've now secured verified factory pricing from three OEM manufacturers — sharing the comparison below:

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

All units use LiFePO4 battery, pure sine wave inverter. Minimum order 50-100 units per model. 7-35 day production.

We handle factory verification, pricing negotiation, quality inspection, and logistics across the Middle East.

Are you currently sourcing portable power stations? Happy to discuss your requirements.

Pen
nichenexusglobal.com"""

body_sea = body_me.replace("Middle East", "Southeast Asia")
body_global = body_me.replace("Middle East", "your region")

region_map = {
    "info@powernsun.com": body_me,
    "dubai@ecosmart-intl.com": body_me,
    "inquiries@solarphilippines.ph": body_sea,
    "sales@luminoussolar.com": body_sea,
    "customercare@su-kam.com": body_sea,
    "info@utl.co.in": body_sea,
    "candra.hermawan@selis.co.id": body_sea,
    "cskh@thegioididong.com": body_sea,
    "support@invertersupply.com": body_global,
    "info@thesolarstore.com": body_global,
    "info@solarpanelstore.com": body_global,
}

subject = "Portable Power Stations: 3-Factory Price Comparison (600W-2500W)"

context = ssl.create_default_context()
sent = 0
errors = []

print(f"Sending to {len(targets)} targets...\n")

for target_email, company in targets:
    body = region_map[target_email]
    
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["From"] = f"Pen <{EMAIL}>"
        msg["To"] = target_email
        msg["Subject"] = subject
        
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as s:
            s.ehlo()
            s.login(EMAIL, PASSWORD)
            s.sendmail(EMAIL, [target_email], msg.as_string())
        
        print(f"  SENT: {target_email} ({company})")
        sent += 1
        time.sleep(7)  # Conservative rate for Tencent
        
    except Exception as e:
        err = str(e)[:150]
        print(f"  FAIL: {target_email} ({company}): {err}")
        errors.append((target_email, company, err))
        time.sleep(3)

print(f"\nDONE: {sent} sent, {len(errors)} failed")
if errors:
    for e, n, err in errors:
        print(f"  FAIL: {e} ({n}): {err}")
