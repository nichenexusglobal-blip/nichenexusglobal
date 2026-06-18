#!/usr/bin/env python3
"""Send 4 cold emails to portable power station distributors."""
import sys, os
sys.path.insert(0, "D:/nichenexusglobal")

from universal_send_gate import send_email

# === EMAIL 1: BatteriQ (Kenya) ===
batteriq_body = """Hello Team at BatteriQ Kenya,

BatteriQ is Kenya's #1 authorised EcoFlow and BLUETTI dealer — you sell EcoFlow DELTA Pro (~KES 350,000+), RIVER 2 Pro, BLUETTI AC500 (KES 84,499), and AC200P, with prices ranging from KES 27,259 to KES 1,049,999.

We offer equivalent LiFePO4 portable power stations at factory-direct pricing that could complement your existing brand lineup as a private-label or secondary brand option.

Our verified factory FOB pricing:
- MECO 1KWH (1000Wh): USD 145/unit
- MECO 2KWH (2000Wh): USD 165/unit
- Anern 1280Wh: USD 205/unit
- Pecron E600LFP (614Wh): USD 168.5/unit
- PowerLFP 1152Wh: USD 219/unit

All LiFePO4 chemistry, comparable capacity to your EcoFlow DELTA and BLUETTI lines at a fraction of the wholesale cost. With your existing M-Pesa payment infrastructure and same-day Nairobi delivery setup, adding these as a budget-friendly house brand would be seamless.

Interested in spec sheets and FOB quotations?

Pen
nichenexusglobal.com"""

# === EMAIL 2: ADEX International (UAE) ===
adex_body = """Hello Team at ADEX International,

ADEX International is an established industrial machinery supplier in Dubai/UAE, serving the region's growing industrial and energy sectors.

With UAE's increasing demand for reliable backup power — both for residential and commercial applications — portable power stations and solar generators represent a natural expansion category for your product line.

Our verified factory FOB pricing for LiFePO4 portable power stations:
- MECO 1KWH (1000Wh): USD 145/unit
- MECO 2KWH (2000Wh): USD 165/unit
- Anern 1280Wh: USD 205/unit
- Pecron E600LFP (614Wh): USD 168.5/unit
- PowerLFP 1152Wh: USD 219/unit

These are factory-direct prices (FOB Shenzhen). The UAE retail market for similar-capacity units runs AED 2,500-5,500 (USD 680-1,500), offering substantial margin opportunity.

Would you like spec sheets and formal FOB quotations?

Pen
nichenexusglobal.com"""

# === EMAIL 3: BLUETTI Nigeria (follow-up, already sent once) ===
bluetti_body = """Hello BLUETTI Nigeria Team,

We previously reached out — following up in case it was missed. You sell BLUETTI AC200P (₦1,034,999), AC300 (₦1,097,999), AC500 (₦2,122,999), EB150 (₦640,999), and AC180 (₦892,999) through ng.bluettipower.com.

We offer factory-direct LiFePO4 portable power stations that could serve as a complementary or private-label line alongside your BLUETTI brand.

Our verified factory FOB pricing:
- MECO 1KWH (1000Wh): USD 145/unit
- MECO 2KWH (2000Wh): USD 165/unit
- Anern 1280Wh: USD 205/unit
- Pecron E600LFP (614Wh): USD 168.5/unit
- PowerLFP 1152Wh: USD 219/unit

At your current AC200P retail of ₦1,034,999 (~USD 1,650), a 1000Wh equivalent from our factory supply at USD 145 FOB represents a significant margin opportunity.

Interested in spec sheets and formal quotations?

Pen
nichenexusglobal.com"""

# === EMAIL 4: Enable PH / EcoFlow Philippines ===
enable_body = """Hello Enable PH / EcoFlow Philippines Team,

Enable PH is the official distributor and operator of ecoflowpower.ph in the Philippines — you sell EcoFlow DELTA Pro (₱231,290), DELTA 2 (₱45,990), RIVER 2 Pro (₱23,990), and more from your Mandaluyong operations.

We offer equivalent LiFePO4 portable power stations at factory-direct pricing that could strengthen your position as a comprehensive power solutions distributor in the Philippines.

Our verified factory FOB pricing:
- MECO 1KWH (1000Wh): USD 145/unit
- MECO 2KWH (2000Wh): USD 165/unit
- Anern 1280Wh: USD 205/unit
- Pecron E600LFP (614Wh): USD 168.5/unit
- PowerLFP 1152Wh: USD 219/unit

Your DELTA 2 retails at ₱45,990 (~USD 790). A comparable-capacity unit from our factory supply at USD 145-205 FOB could open a parallel mid-market or private-label segment.

Interested in spec sheets and formal FOB quotations?

Pen
nichenexusglobal.com"""

# ===== SEND =====
results = []

print("=" * 60)
print("SENDING 4 COLD EMAILS TO DISTRIBUTORS")
print("=" * 60)

# 1. BatteriQ
print("\n--- 1/4: BatteriQ Kenya (hello@batteriq.com) ---")
r1 = send_email(
    to="hello@batteriq.com",
    name="BatteriQ Kenya",
    subject="Factory-direct LiFePO4 power stations for BatteriQ Kenya",
    body=batteriq_body,
    category="customer"
)
results.append(("BatteriQ Kenya", "hello@batteriq.com", r1))

# 2. ADEX International
print("\n--- 2/4: ADEX International (info@adexuae.com) ---")
r2 = send_email(
    to="info@adexuae.com",
    name="ADEX International",
    subject="Portable power stations for UAE distribution",
    body=adex_body,
    category="customer"
)
results.append(("ADEX International", "info@adexuae.com", r2))

# 3. BLUETTI Nigeria (follow-up)
print("\n--- 3/4: BLUETTI Nigeria (sale-nga@bluettipower.com) ---")
r3 = send_email(
    to="sale-nga@bluettipower.com",
    name="BLUETTI Nigeria",
    subject="Follow-up: factory-direct LiFePO4 alternatives",
    body=bluetti_body,
    category="customer",
    is_reply=False
)
results.append(("BLUETTI Nigeria", "sale-nga@bluettipower.com", r3))

# 4. Enable PH / EcoFlow Philippines
print("\n--- 4/4: Enable PH / EcoFlow Philippines (distribution@enable.ph) ---")
r4 = send_email(
    to="distribution@enable.ph",
    name="Enable PH",
    subject="Factory-direct LiFePO4 power stations for Philippines distribution",
    body=enable_body,
    category="customer"
)
results.append(("Enable PH", "distribution@enable.ph", r4))

# ===== SUMMARY =====
print("\n" + "=" * 60)
print("SEND RESULTS SUMMARY")
print("=" * 60)
for name, email, success in results:
    status = "✅ SENT" if success else "❌ BLOCKED/FAILED"
    print(f"  {status} | {name:30s} | {email}")
print("=" * 60)
