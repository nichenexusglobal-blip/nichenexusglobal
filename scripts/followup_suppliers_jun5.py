#!/usr/bin/env python3
"""Follow-up emails to suppliers that replied but haven't given quotes yet."""
import smtplib, ssl, time, json
from email.mime.text import MIMEText

SMTP_HOST = "smtp.exmail.qq.com"
SMTP_PORT = 587
USER = "pen@nichenexusglobal.com"
PASS = os.environ.get("NICHE_EMAIL_PASSWORD", "")

def send(to, subject, body):
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

# === 1. SHUNXIANG ENERGY (Eason) ===
# He asked "what other requirements" - give him specific specs
r1 = send(
    "eason@shunxiangenergy.com",
    "Re: RFQ: 1000W / 2000W LiFePO4 Portable Power Station OEM",
    """Hi Eason,

Thanks for your reply. Here are our specific requirements:

Products needed:
1. 1000W LiFePO4 Portable Power Station (960-1024Wh range)
2. 2000W LiFePO4 Portable Power Station (2000-2048Wh range)

Specification requirements:
- AC Output: 220-240V, 50Hz (Pure Sine Wave)
- Battery: LiFePO4, minimum 3500 cycles
- Certifications: CE, RoHS, UN38.3
- Multiple output ports (USB-A, USB-C PD, DC, AC)
- Solar charging input (MC4/XT60)

Quantities:
- Trial order: 2-5 pcs
- Bulk order: 50-100 pcs

Please provide:
- FOB Shenzhen unit price for each model
- MOQ for trial and bulk
- Lead time
- Packing dimensions and weight per unit
- Available certifications

Looking forward to your quotation.

Best regards,
Pen
nichenexusglobal.com"""
)
print(f"[OK] Shunxiang Energy: {'sent' if r1 else 'FAILED'}")

# === 2. WORLDPOWER (Dora) ===
# She asked about our channel and location
r2 = send(
    "info@wpbattery.com",
    "Re: RFQ: 1000W LiFePO4 Portable Power Station OEM",
    """Hi Dora,

Thanks for your response.

To answer your questions: We are a sourcing company based in Shenzhen — we connect distributors and retailers across Southeast Asia, the Middle East, and Africa with verified Chinese OEM manufacturers. Our clients include retail chains, online sellers, solar installers, and distributors in these markets.

We focus on LiFePO4 portable power stations — currently we have buyers interested in 1000Wh capacity units for sale in SE Asia and Africa.

Could you please share:
- FOB Shenzhen unit price for your 1000Wh LiFePO4 model
- MOQ options (sample vs bulk)
- Product datasheet with dimensions, weight, and certifications
- Lead time

Since we're both in Shenzhen area, we can potentially arrange a visit to discuss partnership further.

Best regards,
Pen
nichenexusglobal.com"""
)
print(f"[OK] WorldPower: {'sent' if r2 else 'FAILED'}")

time.sleep(2)

# === 3. ONESUN PV (Jomi) ===
# He keeps pushing WhatsApp but per Pen's rule: suppliers use email, WhatsApp is for nails only
# Send a very direct, complete RFQ that leaves no room for "talk on WhatsApp" deflection
r3 = send(
    "jomi@onesunpv.com",
    "Re: Following up — FOB quotation for portable power stations (detailed specs enclosed)",
    """Hi Jomi,

I understand you prefer WhatsApp, but to keep all pricing records clear for our buyers, I need formal written quotations via email.

Here are the exact products and quantities we need pricing for:

1. 500W/550Wh LiFePO4 Portable Power Station — 10 pcs trial
2. 1000W/1000Wh LiFePO4 Portable Power Station — 10 pcs trial  
3. 2000W/2000Wh LiFePO4 Portable Power Station — 10 pcs trial

Specifications required:
- AC Output: 220-240V, 50Hz Pure Sine Wave
- Battery: LiFePO4, 3500+ cycles
- Certifications: CE, RoHS
- Solar input capability

Please quote FOB Shenzhen per unit for each model, including:
- Unit price at 10 pcs
- Unit price at 50 pcs
- Unit price at 100 pcs
- MOQ per model
- Lead time
- Packing specs (CBM and gross weight per unit)

We have buyers across SE Asia, Middle East, and Africa actively looking for these products. With written pricing, we can move forward quickly.

Best regards,
Pen
nichenexusglobal.com"""
)
print(f"[OK] OneSun PV: {'sent' if r3 else 'FAILED'}")

time.sleep(2)

# Log to send_log.jsonl
log_entry = json.dumps({
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    "followups": ["Shunxiang Energy", "WorldPower", "OneSun PV"]
}, ensure_ascii=False)

import os
log_path = os.path.expanduser("~/nichenexusglobal/send_log.jsonl")
with open(log_path, "a") as f:
    f.write(log_entry + "\n")

print(f"\nDone. 3 follow-ups sent.")
print(f"Shunxiang: asked for specific FOB pricing on 1000W/2000W LFP")
print(f"WorldPower: answered channel question, asked for 1000Wh FOB pricing")
print(f"OneSun PV: detailed 3-model RFQ bypassing WhatsApp, asked for formal email quote")
