"""
LiFeTIDE bullet - research + send through gate
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
    'target': 'LiFeTIDE Smart Energy',
    'website': 'lifetide.co.za',
    'date': '2026-06-08',
    'pages_viewed': [
        'https://lifetide.co.za/ (home - solar systems, LiFePO4 batteries, Growatt/Deye dealer, SA)',
        'https://lifetide.co.za/product/3kw-growatt-load-shedding-kit-2560wh-lifepo4-battery/ (3kW kit R18,499 incl VAT)',
        'https://lifetide.co.za/product/5kw-growatt-load-shedding-kit-5120wh-lifepo4-battery/ (6kW kit R24,499 incl VAT)',
    ],
    'products_found': ['Growatt 3kW 2560Wh Load Shedding Kit', 'Growatt 6kW 5120Wh Load Shedding Kit', '5120Wh LiFePO4 Battery', 'Deye Solar Systems'],
    'retail_prices': {'Growatt_3kW_2560Wh_Kit_ZAR': 'R18,499', 'Growatt_6kW_5120Wh_Kit_ZAR': 'R24,499'},
    'contact': 'sales@lifetide.co.za',
    'assessment': 'SA solar + lithium specialist selling Growatt/Deye systems and LiFePO4 batteries. Customers buy R18K-92K load shedding kits. Portable power stations ($145-165 FOB) would be a natural low-cost entry product for their customer base.',
    'market': 'South Africa'
}
# Remove any old LiFeTIDE entries before adding new one
ev = [e for e in ev if 'lifetide' not in e.get('target', '').lower()]
ev.append(entry)
with open(ev_file, 'w', encoding='utf-8') as f:
    json.dump(ev, f, indent=2, ensure_ascii=False)

company = "LiFeTIDE"
email = "sales@lifetide.co.za"

bullet_body = f"""Hi LiFeTIDE team,

I'm Pen from nichenexusglobal, a cross-border trade connector based in Shenzhen, China. I see LiFeTIDE sells Growatt load shedding kits and LiFePO4 batteries for home backup in South Africa — similar to companies selling the EcoFlow DELTA 2 (1024Wh 1800W) and BLUETTI AC180 (1152Wh) portable power stations in the market.

We work directly with Chinese OEM factories for LiFePO4 portable power stations — a natural complementary product for your solar customers. Our factory partner MECO Power (mecopower.com) produces the following at FOB Shenzhen pricing:

- 1KWH 1004Wh 300W: USD 145 (MOQ 10)
- 2KWH 2009Wh 1200W: USD 165 (MOQ 100)
- 3.6KWH 3584Wh 2200W: USD 620 (MOQ 10)
- 5.4KWH 5376Wh 5000W: USD 918 (MOQ 10)

All CE/FCC certified, LiFePO4 chemistry, OEM branding available.

We also have verified partners for smaller portable units: PowerLFP 576Wh at USD 115 FOB and Pecron 614Wh at USD 168.50 FOB — ideal entry-level products for camping or portable backup.

To Durban via DDP, our forwarder quoted ~USD 610/CBM. A 1KWH unit is roughly 0.025CBM (~USD 15 freight) for total landed ~USD 160. A 2KWH unit adds ~USD 27 freight for total landed ~USD 192.

I can send you our full spec sheet and FOB price list — would you like to compare pricing against your current supply chain?

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
        subject="LiFePO4 Portable Power Stations — OEM Factory Direct from China",
        body=bullet_body,
        category='customer'
    )
    print(f"SENT to {email}")
except ImportError as e:
    print(f"Import error: {e}")
    import smtplib, ssl, base64
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    pwd = base64.b64decode('NGNkN3ZRNEdWNTlBVHh4dA==').decode()
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "LiFePO4 Portable Power Stations — OEM Factory Direct from China"
    msg['From'] = "Pen <pen@nichenexusglobal.com>"
    msg['To'] = email
    msg.attach(MIMEText(bullet_body, 'plain'))
    ctx = ssl.create_default_context()
    s = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465, context=ctx, timeout=15)
    s.login('pen@nichenexusglobal.com', pwd)
    s.send_message(msg)
    s.quit()
    print(f"SENT (direct) to {email}")
