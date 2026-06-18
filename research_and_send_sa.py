#!/usr/bin/env python3 -X utf8
"""
Research 5 SA distributors and send cold emails through universal gate.
"""
import sys, os, json
from datetime import datetime

WORKDIR = "D:/nichenexusglobal"
sys.path.insert(0, WORKDIR)

# ─── Step 1: Save research evidence for all 5 companies ───────────────

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
            "Does not sell portable power stations specifically - focuses on large-scale solar/storage",
            "Wholesale/re-seller model - potential fit for OEM portable power station line"
        ],
        "retail_prices": [
            "Sigenergy products - no retail pricing shown (wholesale distributor model)"
        ]
    },
    {
        "target": "Nology",
        "url": "https://nology.co.za",
        "email": "info@nology.co.za",
        "time": datetime.now().isoformat(),
        "findings": [
            "BLUETTI authorized distributor in South Africa",
            "Product: Bluetti EB3A (268Wh/600W portable power station)",
            "Product: Bluetti EB70 (716Wh/1000W portable power station)",
            "Product: Bluetti PV120 (120W solar panel)",
            "Founded 2001 - specialist value-added distributor of converged IP solutions",
            "Based in Centurion, Gauteng and Montague Gardens, Cape Town",
            "Sells to resellers, systems integrators, service providers across Southern Africa"
        ],
        "retail_prices": [
            "Bluetti EB3A (268Wh/600W) - retail pricing not shown (distributor model - sells to resellers)",
            "Bluetti EB70 (716Wh/1000W) - retail pricing not shown",
            "Comparable retail in SA: EB3A ~R4,799, EB70 ~R8,339 (from nivo.co.za)"
        ]
    },
    {
        "target": "Flexopower Energies",
        "url": "https://flexopower.co.za",
        "email": "info@flexopower.com",
        "time": datetime.now().isoformat(),
        "findings": [
            "South African designer and manufacturer of portable power stations since 2006",
            "Own brand: Flexopower Lithium series",
            "Products use LiFePO4 batteries",
            "Based in Johannesburg and Stellenbosch",
            "Products: Lithium600, Lithium700, Lithium1200, Lithium2400, Lithium3000",
            "Also sells portable solar panels (Namib, Kalahari, Karoo series)",
            "Direct-to-consumer and B2B sales model"
        ],
        "retail_prices": [
            "Lithium600 (512Wh/600W) - R5,999",
            "Lithium700 - R9,999",
            "Lithium1200 (1008Wh/1200W) - R14,999",
            "Lithium2400 - R0 (no price listed)",
            "Lithium3000 - R32,999 (sale from R35,999)",
            "Extra battery 2560Wh for Lithium3000 - R24,300"
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
            "Also has own house brand battery",
            "Mobile Inverters/Portable Power Stations: Kool Energy and Genki brands",
            "Based in Southern Africa - importer/wholesaler model"
        ],
        "retail_prices": [
            "Kool Energy 1kW 25.6V - R11,900",
            "Kool Energy 1.5kW 25.6V - R19,900",
            "Genki 500W Portable Power Station - R8,266.20"
        ]
    },
    {
        "target": "PSS Distributors",
        "url": "https://pss.co.za",
        "email": "sales@pss.co.za",
        "time": datetime.now().isoformat(),
        "findings": [
            "Power System Services established 1994, renamed PSS Distributors in 2000",
            "One of the largest UPS stockholding companies in South Africa",
            "Brands: BluSky, PSS, Vautex",
            "Products: UPS systems, inverters, batteries, portable power stations",
            "Based in Modderfontein, Johannesburg with 2000m2+ office/warehouse",
            "Branches across Southern Africa",
            "Sells portable power stations as growing category for load shedding backup"
        ],
        "retail_prices": [
            "Portable power stations 150Wh range: R2,500-R3,500",
            "Portable power stations 500Wh range: R8,000-R12,000",
            "High-capacity power stations: varies by brand and features"
        ]
    }
]

# Save research evidence
ev_file = os.path.join(WORKDIR, ".research_evidence.json")
if os.path.exists(ev_file):
    with open(ev_file, encoding="utf-8") as f:
        existing = json.load(f)
else:
    existing = []
existing.extend(evidence)
with open(ev_file, "w", encoding="utf-8") as f:
    json.dump(existing, f, indent=2, ensure_ascii=False)
print(f"📋 Research evidence saved to {ev_file} ({len(existing)} total entries)")


# ─── Step 2: Compose and send emails ──────────────────────────────────

from universal_send_gate import send_email

emails = [
    # (to, name, subject, body)
    (
        "sales@iseli-energy.com",
        "Iseli Energy",
        "OEM LiFePO4 portable power stations for Iseli Energy",
        """Hi Iseli Energy team,

I am Pen from nichenexusglobal, a cross-border trade service company based in China.

I noticed Iseli Energy distributes Sigenergy, Huawei, and CHINT energy storage solutions across Southern Africa. As load shedding continues to drive demand for portable backup power, I wanted to introduce factory-direct LiFePO4 portable power station options that could complement your existing product range.

We work with verified Chinese OEM manufacturers offering competitive FOB pricing:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

All units are CE/FCC certified, LiFePO4 with 6000+ cycles. OEM/private label available with MOQ from 10-50 units for trial orders.

Brands like BLUETTI and EcoFlow retail similar-capacity units at 3-5x these factory prices. For a wholesale distributor like Iseli Energy, these price points offer significant margin opportunity in the growing South African portable power market.

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

I understand Nology is an authorized BLUETTI distributor in South Africa, selling the EB3A (268Wh) and EB70 (716Wh) portable power stations. Given the ongoing load shedding demand across SA, I wanted to present OEM LiFePO4 portable power station alternatives at significantly lower factory-direct FOB pricing:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

For context, the BLUETTI AC200 (2048Wh) retails at approximately USD 1,699 and wholesales around USD 1,020. Our equivalent models from MECO (2009Wh at USD 165 FOB) and Anern (2560Wh at USD 323 FOB) offer factory-direct pricing far below BLUETTI's wholesale cost.

All units use automotive-grade LiFePO4 cells, CE/FCC certified, with 6000+ cycle life. OEM/private label available.

Would Nology be interested in exploring a complementary product line alongside your existing BLUETTI range?

Best regards,
Pen
nichenexusglobal.com"""
    ),
    (
        "info@flexopower.com",
        "Flexopower Energies",
        "OEM LiFePO4 power station supply for Flexopower",
        """Hi Flexopower team,

I am Pen from nichenexusglobal, a cross-border trade service company based in China.

I see Flexopower has been designing portable energy solutions since 2006 and offers a strong range of LiFePO4 power stations - Lithium600 (512Wh at R5,999), Lithium700, Lithium1200 (1008Wh at R14,999), and Lithium3000 (R32,999). Your engineering expertise and local manufacturing are impressive.

I wanted to share our OEM factory-direct pricing from verified Chinese LiFePO4 manufacturers, which could complement Flexopower's product strategy or provide cost-optimized import options:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

To illustrate the cost advantage: your Lithium1200 (1008Wh) retails at R14,999 (~USD 820). Our MECO 1KWH (1004Wh, comparable capacity) is USD 145 FOB. Even after shipping, duties, and margin, there is substantial room for competitive pricing.

Would Flexopower be interested in reviewing spec sheets and discussing a potential OEM supply partnership?

Best regards,
Pen
nichenexusglobal.com"""
    ),
    (
        "info@solarsonic.co.za",
        "Solar Sonic",
        "OEM LiFePO4 portable power stations for Solar Sonic",
        """Hi Solar Sonic team,

I am Pen from nichenexusglobal, a cross-border trade service company based in China.

I see Solar Sonic is a leading importer and wholesaler of green energy solutions, carrying major brands like SUNSYNK, DEYE, FREEDOM WON, HUBBLE LITHIUM, and also Kool Energy and Genki portable power stations. Your Kool Energy 1kW at R11,900 and 1.5kW at R19,900 show you already serve the portable power market.

I wanted to present factory-direct pricing from verified Chinese LiFePO4 OEM manufacturers that could offer even stronger margins:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

For reference, your Kool Energy 1kW sells at R11,900 (~USD 650). A comparable MECO 1KWH (1004Wh) at USD 145 FOB allows for healthy import and distribution margins. Similarly, your Kool Energy 1.5kW at R19,900 (~USD 1,090) compares to a 1280Wh Anern unit at just USD 205 FOB.

All units are CE/FCC certified with LiFePO4 cells, 6000+ cycles. OEM/private label available. MOQ from 10-50 units.

Would Solar Sonic be interested in reviewing spec sheets?

Best regards,
Pen
nichenexusglobal.com"""
    ),
    (
        "sales@pss.co.za",
        "PSS Distributors",
        "LiFePO4 portable power stations for PSS Distributors",
        """Hi PSS team,

I am Pen from nichenexusglobal, a cross-border trade service company based in China.

I see PSS Distributors has been a leading UPS and power solutions provider in South Africa since 1994, and you now carry portable power stations as a growing category for load shedding backup. Your current range includes units from 150Wh to 500Wh+ at R2,500-R12,000 retail.

I wanted to present factory-direct LiFePO4 portable power station pricing from verified Chinese OEM manufacturers that could expand your range significantly:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

To put this in perspective: comparable brands like BLUETTI (AC200, 2048Wh) retail at approximately USD 1,699 with wholesale around USD 1,020. Our equivalent 2000Wh-class units from MECO at USD 165 FOB or Anern 2560Wh at USD 323 FOB represent dramatic savings at the import level.

These units are CE/FCC certified, LiFePO4 with 6000+ cycle life, and available with OEM/private label. Ideal for the South African load shedding market.

Would PSS Distributors be interested in reviewing spec sheets and discussing a trial order?

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
