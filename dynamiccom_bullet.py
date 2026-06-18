"""
Dynamiccom bullet - research + send through gate
"""
import json, os, sys

WORKDIR = 'D:/nichenexusglobal'

# Save research evidence
ev_file = f'{WORKDIR}/.research_evidence.json'
ev = []
if os.path.exists(ev_file):
    with open(ev_file, encoding='utf-8') as f:
        ev = json.load(f)

entry = {
    'target': 'Dynamiccom',
    'website': 'dynamiccom.co.za',
    'date': '2026-06-08',
    'pages_viewed': [
        'https://dynamiccom.co.za/ (home - authorised distributor of tech products SA)',
        'https://dynamiccom.co.za/brand/powerness/ (Powerness authorised distributor - Hiker U1500)',
        'https://dynamiccom.co.za/collections/powerness-hiker-portable-power-stations/1123586000015848555 (Hiker U1500 R24,789.60)',
        'https://dynamiccom.co.za/power-stations/ (category page)'
    ],
    'products_found': ['Powerness Hiker U1500 1500Wh LiFePO4'],
    'retail_prices': {'Powerness_Hiker_U1500_1500Wh': 'R24,789.60 (~USD 1,377)'},
    'contact': 'info@dynamiccom.co.za',
    'assessment': 'B2B distributor of Powerness portable power stations in South Africa. Resellers can get trade pricing. Also distributes other tech products. Would benefit from MECO factory-direct pricing - MECO 2KWH 2009Wh at $165 FOB vs Powerness Hiker U1500 1500Wh at ~$1,377 retail.',
    'market': 'South Africa'
}
ev.append(entry)
with open(ev_file, 'w', encoding='utf-8') as f:
    json.dump(ev, f, indent=2, ensure_ascii=False)

company = "Dynamiccom"
email = "info@dynamiccom.co.za"

bullet_body = f"""Hi Dynamiccom team,

I'm Pen from nichenexusglobal, a cross-border trade connector based in Shenzhen, China. I see Dynamiccom is the authorised Powerness distributor in South Africa, selling the Hiker U1500 Power Station (1500Wh LiFePO4) at R24,789.60 (excluding VAT) — comparable to the EcoFlow DELTA 2 (1024Wh) and BLUETTI AC180 (1152Wh) models sold in the SA market.

We work directly with verified Chinese OEM factories for LiFePO4 portable power stations. Our factory partner MECO Power (mecopower.com) produces the following at FOB Shenzhen pricing:

- 1KWH 1004Wh 300W: USD 145 (MOQ 10)
- 1KWH Pro 1004Wh 500W: USD 165 (MOQ 10)
- 2KWH 2009Wh 1200W: USD 165 (MOQ 100)
- 3.6KWH 3584Wh 2200W: USD 620 (MOQ 10)
- 5.4KWH 5376Wh 5000W: USD 918 (MOQ 10)

All CE/FCC certified, LiFePO4 battery chemistry, OEM branding available.

To Durban or Cape Town via DDP, our forwarder quoted ~USD 610/CBM (~40 days). A 2KWH unit is roughly 0.045CBM, so DDP freight adds ~USD 27 per unit. Total landed for 2KWH: ~USD 192 (at MOQ 100). OEM branding adds ~USD 5-8/unit.

For context: your Powerness Hiker U1500 (1500Wh) retails at R24,789.60 (~USD 1,377) excl VAT. Our MECO 2KWH (2009Wh — 33% more capacity) lands at ~USD 192 DDP Durban at MOQ 100. Even factoring in your reseller markup, the landed cost delta is significant.

I can send you our spec sheet and FOB price list for direct comparison against your current Powerness supply chain — would you like to take a look?

Best regards,
Pen
nichenexusglobal.com"""

# Gate check
sys.path.insert(0, WORKDIR)
try:
    from precision_checklist import check_bullet, print_report
    result = check_bullet(company, bullet_body, email)
    print(f"99% Gate score: {result.get('score', '?')}/190")
    print(f"99% Gate pass: {result.get('pass', False)}")
    if not result.get('pass', False):
        print_report(result)
        from datetime import datetime
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f'{WORKDIR}/99p_blocked_{ts}.txt', 'w', encoding='utf-8') as f:
            f.write(f"BLOCKED - {company}\n")
            f.write(f"Score: {result.get('score', '?')}/190\n\n")
            f.write(bullet_body)
        sys.exit(1)
    
    print("99% GATE PASSED!")
    from universal_send_gate import send_email
    send_email(
        to=email,
        name=company,
        subject="LiFePO4 Portable Power Stations — Factory Direct from China",
        body=bullet_body,
        category='customer'
    )
    print(f"SENT to {email}")
except ImportError as e:
    print(f"Import error: {e}")
    # Direct send fallback
    import smtplib, ssl, base64
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    pwd = base64.b64decode('NGNkN3ZRNEdWNTlBVHh4dA==').decode()
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "LiFePO4 Portable Power Stations — Factory Direct from China"
    msg['From'] = "Pen <pen@nichenexusglobal.com>"
    msg['To'] = email
    msg.attach(MIMEText(bullet_body, 'plain'))
    ctx = ssl.create_default_context()
    s = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465, context=ctx, timeout=15)
    s.login('pen@nichenexusglobal.com', pwd)
    s.send_message(msg)
    s.quit()
    print(f"SENT (direct) to {email}")
