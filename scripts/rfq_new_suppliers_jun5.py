#!/usr/bin/env python3
"""Send RFQs to new suppliers found today (June 5)."""
import smtplib, ssl, time, json

SMTP_HOST = "smtp.exmail.qq.com"
SMTP_PORT = 587
USER = "pen@nichenexusglobal.com"
PASS = os.environ.get("NICHE_EMAIL_PASSWORD", "")

def send(to, subject, body):
    from email.mime.text import MIMEText
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = f"Pen <{USER}>"
    msg["To"] = to
    msg["Subject"] = subject
    ctx = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as s:
        s.starttls(context=ctx)
        s.login(USER, PASS)
        s.send_message(msg)
    return True

log_entries = []

# RFQ template body
def rfq_body(cat="1000W-2000W LiFePO4 Portable Power Station"):
    return f"""Hi Team,

I am Pen from nichenexusglobal, a sourcing company helping distributors and retailers in Southeast Asia, Middle East, and Africa source high-quality portable power stations.

We are currently looking for OEM/ODM partners for LiFePO4 portable power stations in the following categories:

Products needed:
1. 500W / 500-700Wh LiFePO4 Portable Power Station
2. 1000W / 960-1100Wh LiFePO4 Portable Power Station
3. 2000W / 2000-2100Wh LiFePO4 Portable Power Station

Specifications:
- AC Output: 220-240V, 50Hz Pure Sine Wave
- Battery: LiFePO4, minimum 3500 cycles
- Certifications: CE, RoHS, UN38.3
- Multi-output: USB-A, USB-C PD, DC, AC
- Solar charging input

Please provide:
- FOB Shenzhen unit price for each model
- MOQ for trial (2-5 pcs) and bulk (50-100 pcs)
- Lead time
- Packing dimensions and gross weight per unit
- Available certifications

Looking forward to your quotation.

Best regards,
Pen
nichenexusglobal.com"""

# ======== 1. iFlowPower ========
# 300W-2000W range, OEM/ODM, contact@iflowpower.com, +86 18988945661
send("contact@iflowpower.com",
    "RFQ: 500W / 1000W / 2000W LiFePO4 Portable Power Station OEM",
    rfq_body())
print("[1/8] iFlowPower - sent")
log_entries.append({"company": "iFlowPower", "email": "contact@iflowpower.com"})
time.sleep(3)

# ======== 2. Witroy Solar ========
# Shenzhen, 300W LiFePO4, info@witroy.com
send("info@witroy.com",
    "RFQ: 500W / 1000W LiFePO4 Portable Power Station OEM",
    rfq_body("500W-1000W"))
print("[2/8] Witroy Solar - sent")
log_entries.append({"company": "Witroy Solar", "email": "info@witroy.com"})
time.sleep(3)

# ======== 3. Bicodi ========
# Shenzhen, 300W-3000W, sales@bicodi.com
send("sales@bicodi.com",
    "RFQ: 1000W / 2000W LiFePO4 Portable Power Station OEM",
    rfq_body())
print("[3/8] Bicodi - sent")
log_entries.append({"company": "Bicodi", "email": "sales@bicodi.com"})
time.sleep(3)

# ======== 4. Beston ========
# Dongguan, 2000W/1920Wh, daisy@beston-energy.com
send("daisy@beston-energy.com",
    "RFQ: 500W / 1000W / 2000W LiFePO4 Portable Power Station OEM/ODM",
    rfq_body())
print("[4/8] Beston - sent")
log_entries.append({"company": "Beston", "email": "daisy@beston-energy.com"})
time.sleep(3)

# ======== 5. DC Power Factory ========
# Shenzhen, 500W+, info@dcpowerfactory.com
send("info@dcpowerfactory.com",
    "RFQ: 500W / 1000W LiFePO4 Portable Power Station OEM",
    rfq_body("500W-1000W"))
print("[5/8] DC Power Factory - sent")
log_entries.append({"company": "DC Power Factory", "email": "info@dcpowerfactory.com"})
time.sleep(3)

# ======== 6. LiFePower (powerlfp.com) ========
# Shenzhen, office@powerlfp.com
send("office@powerlfp.com",
    "RFQ: 500W / 1000W / 2000W LiFePO4 Portable Power Station OEM",
    rfq_body())
print("[6/8] LiFePower - sent")
log_entries.append({"company": "LiFePower", "email": "office@powerlfp.com"})
time.sleep(3)

# ======== 7. GreFlow Energy ========
# Shenzhen/Dongguan, eva@amazing-battery.com
send("eva@amazing-battery.com",
    "RFQ: 1000W / 2000W LiFePO4 Portable Power Station OEM",
    rfq_body())
print("[7/8] GreFlow Energy - sent")
log_entries.append({"company": "GreFlow Energy", "email": "eva@amazing-battery.com"})
time.sleep(3)

# ======== 8. LifePO4 Powers ========
# Shenzhen, info@lifepo4powers.com
send("info@lifepo4powers.com",
    "RFQ: 1000W / 2000W LiFePO4 Portable Power Station OEM",
    rfq_body())
print("[8/8] LifePO4 Powers - sent")
log_entries.append({"company": "LifePO4 Powers", "email": "info@lifepo4powers.com"})

# Log
import os
log_path = os.path.expanduser("~/nichenexusglobal/send_log.jsonl")
with open(log_path, "a", encoding='utf-8') as f:
    for entry in log_entries:
        entry["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
        entry["category"] = "vendor_rfq"
        entry["success"] = True
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(f"\nDone. 8 new supplier RFQs sent.")
