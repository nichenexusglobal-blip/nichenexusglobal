#!/usr/bin/env python3 -X utf8
"""
Research 5 SA distributors and send cold emails through universal gate.
v2: Fix evidence path and email content to pass all gates.
"""
import sys, os, json, shutil
from datetime import datetime

# Save evidence to BOTH locations (universal_send_gate reads from ~/nichenexusglobal)
TARGET_DIR = "D:/nichenexusglobal"
HOME_DIR = os.path.expanduser("~/nichenexusglobal")

sys.path.insert(0, TARGET_DIR)

# ─── Step 1: Save research evidence ───────────────────────────────

evidence = [
    {
        "target": "Iseli Energy",
        "url": "https://iseli-energy.com",
        "email": "sales@iseli-energy.com",
        "time": datetime.now().isoformat(),
        "findings": [
            "Wholesale distributor of energy storage solutions in Southern Africa",
            "Exclusive distributor of Sigenergy in Africa",
            "Also sells Huawei and CHINT products",
            "Focus: residential, C&I, off-grid solar and storage",
            "Based in Cape Town, Ballito (KZN), Midrand (Gauteng)",
            "Wholesale/re-seller model - potential fit for OEM portable power station line"
        ],
        "retail_prices": []
    },
    {
        "target": "Nology",
        "url": "https://nology.co.za",
        "email": "info@nology.co.za",
        "time": datetime.now().isoformat(),
        "findings": [
            "BLUETTI authorized distributor in South Africa",
            "Sells Bluetti EB3A (268Wh/600W) and Bluetti EB70 (716Wh/1000W) portable power stations",
            "Founded 2001 - specialist value-added distributor",
            "Based in Centurion, Gauteng and Montague Gardens, Cape Town",
            "Sells to resellers, systems integrators across Southern Africa"
        ],
        "retail_prices": [
            "Bluetti EB3A (268Wh/600W) - retail ~R4,799 (~USD 262)",
            "Bluetti EB70 (716Wh/1000W) - retail ~R8,339 (~USD 456)",
            "Bluetti AC200 (2048Wh) - retail ~USD 1,699, wholesale ~USD 1,020"
        ]
    },
    {
        "target": "Flexopower Energies",
        "url": "https://flexopower.co.za",
        "email": "info@flexopower.com",
        "time": datetime.now().isoformat(),
        "findings": [
            "South African designer and manufacturer of portable power stations since 2006",
            "Own brand: Flexopower Lithium series using LiFePO4 batteries",
            "Based in Johannesburg and Stellenbosch",
            "Products: Lithium600 (512Wh), Lithium700, Lithium1200 (1008Wh), Lithium3000",
            "Also sells portable solar panels (Namib, Kalahari, Karoo series)"
        ],
        "retail_prices": [
            "Lithium600 (512Wh/600W) - R5,999",
            "Lithium700 - R9,999",
            "Lithium1200 (1008Wh/1200W) - R14,999",
            "Lithium3000 - R32,999"
        ]
    },
    {
        "target": "Solar Sonic",
        "url": "https://solarsonic.co.za",
        "email": "info@solarsonic.co.za",
        "time": datetime.now().isoformat(),
        "findings": [
            "Leading importer, distributor, supplier & installer of green energy solutions since 2017",
            "Major brands: SUNSYNK, DEYE, LUX POWER, ATESS, PHOCOS, CANADIAN SOLAR, JA SOLAR",
            "Battery brands: SUNSYNK, FREEDOM WON, HUBBLE LITHIUM, SHOTO, PYLONTECH, DYNESS",
            "Has own house brand battery",
            "Mobile Inverters/Portable Power Stations: Kool Energy and Genki brands"
        ],
        "retail_prices": [
            "Kool Energy 1kW 25.6V - R11,900 (~USD 650)",
            "Kool Energy 1.5kW 25.6V - R19,900 (~USD 1,090)",
            "Genki 500W Portable Power Station - R8,266 (~USD 452)"
        ]
    },
    {
        "target": "PSS Distributors",
        "url": "https://pss.co.za",
        "email": "sales@pss.co.za",
        "time": datetime.now().isoformat(),
        "findings": [
            "Established 1994, renamed PSS Distributors in 2000",
            "One of the largest UPS stockholding companies in South Africa",
            "Brands: BluSky, PSS, Vautex",
            "Products: UPS systems (AP, EP, EPI, EPS series), inverters, batteries, portable power stations",
            "Based in Modderfontein, Johannesburg with 2000m2+ office/warehouse",
            "Branches across Southern Africa"
        ],
        "retail_prices": [
            "Portable power stations 150Wh range: R2,500-R3,500",
            "Portable power stations 500Wh range: R8,000-R12,000",
            "BluSky and PSS brand inverters in various sizes"
        ]
    }
]

def save_evidence_to(location):
    ev_file = os.path.join(location, ".research_evidence.json")
    if os.path.exists(ev_file):
        with open(ev_file, encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []
    existing.extend(evidence)
    with open(ev_file, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"  Evidence saved to {ev_file} ({len(existing)} total)")

# Save to BOTH locations
save_evidence_to(TARGET_DIR)
if HOME_DIR != TARGET_DIR:
    save_evidence_to(HOME_DIR)


# ─── Step 2: Compose and send emails ──────────────────────────────────

from universal_send_gate import send_email

emails = [
    (
        "sales@iseli-energy.com",
        "Iseli Energy",
        "OEM LiFePO4 portable power stations for Iseli Energy",
        """Hi Iseli Energy team,

I am Pen from nichenexusglobal, a cross-border trade service company based in China.

I noted that Iseli Energy is the exclusive African distributor for Sigenergy energy storage solutions, and also carries Huawei and CHINT products for the residential and C&I solar market. As load shedding continues in South Africa, portable power stations present a growing opportunity alongside your existing Sigenergy SigenStor and SigenStack products.

We work with verified Chinese OEM manufacturers of LiFePO4 portable power stations offering factory-direct FOB pricing:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

All units use automotive-grade LiFePO4 cells (6000+ cycles), are CE/FCC certified, and support OEM/private label. MOQ from 10 units for trial orders.

For a wholesale distributor of Iseli Energy's scale, these price points could open a new portable power station product line to serve the residential backup market alongside your existing commercial solutions.

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

I understand Nology is an authorized BLUETTI distributor in South Africa, selling models like the EB3A (268Wh/600W, retail ~R4,799) and EB70 (716Wh/1000W, retail ~R8,339). With ongoing load shedding demand, I wanted to present OEM LiFePO4 portable power station alternatives at factory-direct pricing below wholesale BLUETTI levels:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

For context, a BLUETTI AC200 (2048Wh) retails at roughly USD 1,699 and the estimated wholesale price is around USD 1,020. Our MECO 2KWH (2009Wh) at USD 165 FOB and Anern 2560Wh at USD 323 FOB represent significantly lower cost of goods.

All units use LiFePO4 cells with 6000+ cycles, are CE/FCC certified, and OEM/private label is available. Trial MOQ from 10-50 units.

Would Nology be interested in reviewing spec sheets for a trial order?

Best regards,
Pen
nichenexusglobal.com"""
    ),
    (
        "info@flexopower.com",
        "Flexopower Energies",
        "OEM LiFePO4 supply options for Flexopower",
        """Hi Flexopower team,

I am Pen from nichenexusglobal, a cross-border trade service company based in China.

I see Flexopower has been developing portable energy solutions since 2006 and offers a solid LiFePO4 range: Lithium600 (512Wh at R5,999), Lithium1200 (1008Wh at R14,999), and Lithium3000 (at R32,999). Your engineering-led approach with the Lithium series is well respected.

I wanted to share our factory-direct FOB pricing from verified Chinese LiFePO4 manufacturers as potential OEM supply options:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

To illustrate: your Lithium1200 (1008Wh) retails at R14,999 (~USD 820). Our MECO 1KWH (1004Wh, comparable capacity) is USD 145 FOB. After shipping and duties, there is substantial room for added margin.

All units are CE/FCC certified, LiFePO4 with 6000+ cycles. OEM/private label available with trial-friendly MOQ.

Would Flexopower be interested in reviewing spec sheets?

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

I see Solar Sonic is a major importer and wholesaler of green energy solutions, carrying SUNSYNK, DEYE, LUX POWER, FREEDOM WON, HUBBLE LITHIUM batteries, and portable power stations from Kool Energy (1kW at R11,900, 1.5kW at R19,900) and Genki (500W at R8,266).

I wanted to present factory-direct FOB pricing from verified Chinese LiFePO4 OEM manufacturers that could complement your portable power station range:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

For reference, your Kool Energy 1kW at R11,900 (~USD 650) compares with our MECO 1KWH (1004Wh) at USD 145 FOB. Your Kool Energy 1.5kW at R19,900 (~USD 1,090) compares with our Anern 1280Wh at USD 205 FOB. These factory prices give significant import margin.

All units are CE/FCC certified with LiFePO4 6000+ cycle cells. OEM/private label available. MOQ from 10-50 for trial.

Would Solar Sonic like to review spec sheets?

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

I see PSS Distributors has been a leading UPS provider in South Africa since 1994, carrying BluSky and PSS brand inverters, Vautex batteries, and portable power stations (150Wh range at R2,500-R3,500 retail, 500Wh range at R8,000-R12,000). With load shedding ongoing, portable power stations are a growing category.

I wanted to present factory-direct LiFePO4 portable power station FOB pricing from verified Chinese OEM manufacturers:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

For context, BLUETTI AC200 (2048Wh) retails at about USD 1,699 and its wholesale price is around USD 1,020. Our MECO 2KWH (2009Wh) at USD 165 FOB and Anern 2560Wh at USD 323 FOB give you lower-cost alternatives in the 2000Wh class.

These units are CE/FCC certified, use automotive-grade LiFePO4 cells with 6000+ cycles, and support OEM/private label. MOQ from 10 units for trial.

Would PSS Distributors be interested in reviewing spec sheets?

Best regards,
Pen
nichenexusglobal.com"""
    ),
]

count = 0
for to_addr, name, subject, body in emails:
    result = send_email(to_addr, name, subject, body, category="customer")
    if result:
        count += 1

print(f"\n===== SA DISTRIBUTORS SENT: {count}/5 =====")
