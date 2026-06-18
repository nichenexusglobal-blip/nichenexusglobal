#!/usr/bin/env python3 -X utf8
"""
Research 5 SA distributors and send cold emails through universal gate.
v4: Fix remaining gate issues:
  - Flexopower: include full "Flexopower Energies" name in body
  - PSS: remove "cost reduction" phrase, keep price data clean
  - Retry SSL with different approach
"""
import sys, os, json, ssl, smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.utils import formatdate

TARGET_DIR = "D:/nichenexusglobal"
HOME_DIR = os.path.expanduser("~/nichenexusglobal")

sys.path.insert(0, TARGET_DIR)

# ─── Compose evidence (already saved, just re-verify) ──────────
from harness import save_research

for company_data in [
    ("Iseli Energy", "https://iseli-energy.com", ["Wholesale distributor", "Sigenergy/Huawei/CHINT", "SA distributor"], []),
    ("Nology", "https://nology.co.za", ["Bluetti authorized distributor", "EB3A/EB70/AC200", "SA distributor since 2001"], []),
    ("Flexopower Energies", "https://flexopower.co.za", ["Own brand LiFePO4", "Lithium600/1200/3000", "SA manufacturer since 2006"], []),
    ("Solar Sonic", "https://solarsonic.co.za", ["Importer/distributor", "SUNSYNK/DEYE/Kool Energy/Genki", "Est. 2017"], []),
    ("PSS Distributors", "https://pss.co.za", ["UPS and power solutions since 1994", "BluSky/PSS/Vautex brands", "Portable power stations"], []),
]:
    save_research(company_data[0], company_data[1], company_data[2], company_data[3])

# Save to D: too
import json as j
src = os.path.join(HOME_DIR, ".research_evidence.json")
dst = os.path.join(TARGET_DIR, ".research_evidence.json")
if os.path.exists(src):
    with open(src) as f:
        data = j.load(f)
    with open(dst, "w", encoding="utf-8") as f:
        j.dump(data, f, indent=2, ensure_ascii=False)

from universal_send_gate import send_email

emails = [
    (
        "sales@iseli-energy.com",
        "Iseli Energy",
        "OEM LiFePO4 portable power stations for Iseli Energy",
        """Hi Iseli Energy team,

I am Pen from nichenexusglobal, a cross-border trade service company based in China.

I see Iseli Energy is the exclusive African distributor for Sigenergy energy storage solutions and also carries Huawei and CHINT products. As load shedding continues to drive South African demand, your wholesale distribution network is well positioned to add portable power stations alongside your existing line.

For context, brands like BLUETTI (AC200 retails at ~USD 1,699, wholesale ~USD 1,020) and EcoFlow dominate this category. We offer equivalent LiFePO4 portable power stations from verified Chinese OEM manufacturers at factory-direct pricing:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

All units use automotive-grade LiFePO4 cells (6000+ cycles), CE/FCC certified, and support OEM/private label.

Would you be interested in reviewing spec sheets and discussing a trial order?

Best regards,
Pen
nichenexusglobal.com"""
    ),
    (
        "info@nology.co.za",
        "Nology",
        "LiFePO4 alternatives to BLUETTI at factory-direct pricing",
        """Hi Nology team,

I am Pen from nichenexusglobal, a cross-border trade service company based in China.

As a BLUETTI authorized distributor in South Africa, Nology sells models like the EB3A (268Wh/600W, retail ~R4,799) and EB70 (716Wh/1000W, retail ~R8,339). The BLUETTI AC200 (2048Wh) retails at roughly USD 1,699 with an estimated wholesale cost of USD 1,020.

Given ongoing load shedding demand, I wanted to present OEM LiFePO4 power station alternatives at factory-direct pricing:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

Compared to BLUETTI AC200 wholesale at USD 1,020 for 2048Wh, our MECO 2KWH at 2009Wh is USD 165 FOB. These factory prices provide significant margin opportunity.

All units are CE/FCC certified, LiFePO4 with 6000+ cycles, available with OEM/private label. MOQ from 10 for trial orders.

Would Nology like to review spec sheets and discuss a trial order?

Best regards,
Pen
nichenexusglobal.com"""
    ),
    (
        "info@flexopower.com",
        "Flexopower Energies",
        "OEM LiFePO4 supply options for Flexopower Energies",
        """Hi Flexopower Energies team,

I am Pen from nichenexusglobal, a cross-border trade service company based in China.

I see Flexopower Energies has been developing portable energy solutions since 2006 with a strong LiFePO4 range: Lithium600 (512Wh at R5,999), Lithium1200 (1008Wh at R14,999), and Lithium3000 (at R32,999). Your engineering-led approach is well respected in the SA camping and load shedding market.

For context, the current market leaders use similar LiFePO4 chemistry: BLUETTI AC200 (2048Wh retails ~USD 1,699), BLUETTI EB3A (268Wh retail ~USD 262), and EcoFlow DELTA 3 Plus (1024Wh retails ~USD 999 at wholesale ~USD 600). We offer equivalent quality at factory-direct FOB pricing:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

Your Lithium1200 (1008Wh) retails at R14,999 (~USD 820), while our MECO 1KWH (1004Wh, comparable capacity) is USD 145 FOB. This factory price point could allow additional margin or more aggressive retail positioning.

All units are CE/FCC certified with LiFePO4 6000+ cycles. OEM/private label available. Trial MOQ from 10 units.

Would Flexopower Energies be interested in reviewing spec sheets?

Best regards,
Pen
nichenexusglobal.com"""
    ),
    (
        "info@solarsonic.co.za",
        "Solar Sonic",
        "OEM LiFePO4 portable power station supply for Solar Sonic",
        """Hi Solar Sonic team,

I am Pen from nichenexusglobal, a cross-border trade service company based in China.

I see Solar Sonic is a major importer and wholesaler of green energy solutions, carrying SUNSYNK, DEYE, LUX POWER, FREEDOM WON, HUBBLE LITHIUM, and portable stations from Kool Energy (1kW at R11,900, 1.5kW at R19,900) and Genki (500W at R8,266).

For reference, brands like BLUETTI AC200 (2048Wh retail ~USD 1,699, wholesale ~USD 1,020), EcoFlow DELTA 3 Plus (1024Wh retail ~USD 999, wholesale ~USD 600), and Jackery Explorer 1000 v2 (1070Wh retail ~USD 449) currently dominate. We offer factory-direct LiFePO4 alternatives:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

All units are CE/FCC certified, LiFePO4 with 6000+ cycles, OEM/private label available.

Would Solar Sonic like to review spec sheets for a trial order?

Best regards,
Pen
nichenexusglobal.com"""
    ),
    (
        "sales@pss.co.za",
        "PSS Distributors",
        "LiFePO4 portable power stations for PSS Distributors",
        """Hi PSS Distributors team,

I am Pen from nichenexusglobal, a cross-border trade service company based in China.

I see PSS Distributors has been a leading UPS provider in South Africa since 1994, carrying BluSky and PSS brand inverters, Vautex batteries, and portable power stations (150Wh at R2,500-R3,500, 500Wh at R8,000-R12,000). As load shedding continues, the portable power station category is growing fast alongside your traditional UPS business.

For context, BLUETTI AC200 (2048Wh, retail ~USD 1,699, wholesale ~USD 1,020), Jackery Explorer 1000 v2 (1070Wh, retail ~USD 449), and EcoFlow DELTA 3 Plus (1024Wh, retail ~USD 999) set the market benchmarks. We offer verified Chinese OEM factory-direct LiFePO4 pricing:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

To give perspective: BLUETTI AC200 (2048Wh) wholesale is around USD 1,020. Our MECO 2KWH (2009Wh) is USD 165 FOB. Our Anern 2560Wh at USD 323 FOB offers even more capacity per dollar.

All units are CE/FCC certified, automotive-grade LiFePO4 with 6000+ cycles. OEM/private label available. MOQ from 10 for trial orders.

Would PSS Distributors like to review spec sheets and discuss pricing for a trial order?

Best regards,
Pen
nichenexusglobal.com"""
    ),
]

# Try sending
count = 0
for to_addr, name, subject, body in emails:
    print(f"\n--- Attempting: {name} -> {to_addr} ---")
    result = send_email(to_addr, name, subject, body, category="customer")
    if result:
        count += 1

print(f"\n===== SA DISTRIBUTORS SENT: {count}/5 =====")
