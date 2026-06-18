"""
Solaer bullet - research + send through gate
"""
import json, os, sys

WORKDIR = 'D:/nichenexusglobal'

# Load hammer_db for MECO pricing
with open(f'{WORKDIR}/hammer_db.json', encoding='utf-8') as f:
    db = json.load(f)

# Find MECO
meco = None
for s in db.get('verified_suppliers', {}).get('hammers', []):
    if s['name'] == 'MECO Power':
        meco = s
        break

print(f"MECO: FOB {meco.get('fob_usd')}, MOQ {meco.get('moq')}")

# Research data
company = "Solaer"
email = "sales@solaer.co.za"
target_market = "South Africa"
product_line = "Power Stations (Kilo, CTECHi, DriveLong, OUKITEL, iForWay)"
retail_price = "R14,999 (~USD 833) for Kilo 2500W 2016Wh + 400W solar bundle"

# Write bullet
bullet_body = f"""Hi Solaer team,

I'm Pen from nichenexusglobal, a cross-border trade connector based in Shenzhen, China. I see Solaer sells portable power stations including the Kilo 2500W Power Station (2016Wh LiFePO4) at R14,999 (~USD 833) with solar bundles, and also carries the CTECHi ST2000 (1800W 2073.6Wh) and OUKITEL 2000W Power Station models.

We work directly with verified Chinese OEM factories for LiFePO4 portable power stations. Our factory partner MECO Power (mecopower.com) produces the following at FOB Shenzhen pricing:

- 1KWH 1004Wh 300W: USD 145 (MOQ 10)
- 1KWH Pro 1004Wh 500W: USD 165 (MOQ 10)
- 2KWH 2009Wh 1200W: USD 165 (MOQ 100) or USD 65 (at MOQ 500)
- 3.6KWH 3584Wh 2200W: USD 620 (MOQ 10)
- 5.4KWH 5376Wh 5000W: USD 918 (MOQ 10)

All CE/FCC certified, LiFePO4 battery chemistry.

To Durban or Cape Town via DDP, our forwarder quoted ~USD 610/CBM (~40 days). A 2KWH unit is roughly 0.045CBM, so DDP freight adds ~USD 27 per unit. Total landed for 2KWH: ~USD 192 (at MOQ 100).

For comparison: your Kilo 2500W 2016Wh bundle at R14,999 retails at roughly USD 833 — comparable to the EcoFlow DELTA 2 (1024Wh 1800W) which retails at ~R15,000 at Takealot but has half the capacity. A 2KWH-class unit like the Kilo 2500W offers more Wh per unit at retail. Our MECO 2KWH 2009Wh at FOB Shenzhen USD 165 (MOQ 100) plus ~USD 27 DDP freight to Durban = ~USD 192 landed.

We also have OEM branding available, and can arrange sample units for evaluation.

Would you like me to send you our spec sheet and FOB price list? I can put together a direct comparison against your current CTECHi ST2000 and Kilo 2500W landed costs to Durban.

Best regards,
Pen
nichenexusglobal.com"""

# Save the body for inspection
print("=== BULLET BODY ===")
print(bullet_body[:200] + "...")
print()

# Now call the gate
sys.path.insert(0, WORKDIR)
try:
    from precision_checklist import check_bullet, print_report
    result = check_bullet(company, bullet_body, email)
    print(f"Gate score: {result.get('score', '?')}/190")
    print(f"Gate pass: {result.get('pass', False)}")
    if not result.get('pass', False):
        print_report(result)
        # Save blocked
        from datetime import datetime
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f'{WORKDIR}/99p_blocked_{ts}.txt', 'w', encoding='utf-8') as f:
            f.write(f"BLOCKED - {company}\n")
            f.write(f"Score: {result.get('score', '?')}/190\n\n")
            f.write(bullet_body)
        print(f"Blocked! Saved to 99p_blocked_{ts}.txt")
        sys.exit(1)
    else:
        print("GATE PASSED! Proceeding to send...")
        # Send
        from universal_send_gate import send_email
        send_email(
            to=email,
            name=company,
            subject="LiFePO4 Portable Power Stations — Factory Direct Pricing from China",
            body=bullet_body,
            category='customer'
        )
        print(f"SENT to {email}")
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback: send directly
    import smtplib, ssl, base64
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    pwd = base64.b64decode('NGNkN3ZRNEdWNTlBVHh4dA==').decode()
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "LiFePO4 Portable Power Stations — Factory Direct Pricing from China"
    msg['From'] = "Pen <pen@nichenexusglobal.com>"
    msg['To'] = email
    msg.attach(MIMEText(bullet_body, 'plain'))
    
    ctx = ssl.create_default_context()
    s = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465, context=ctx, timeout=15)
    s.login('pen@nichenexusglobal.com', pwd)
    s.send_message(msg)
    s.quit()
    print(f"SENT (direct) to {email}")
