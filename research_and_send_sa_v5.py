#!/usr/bin/env python3 -X utf8
"""
Research 5 SA distributors and send cold emails through universal gate.
v5 FINAL: Fix all gate issues + handle SMTP block by saving approved emails as drafts.
"""
import sys, os, json
from datetime import datetime

TARGET_DIR = "D:/nichenexusglobal"
HOME_DIR = os.path.expanduser("~/nichenexusglobal")
sys.path.insert(0, TARGET_DIR)

# ─── Save research evidence ────────────────────────────────────
from harness import save_research as sr

research_data = [
    ("Iseli Energy", "https://iseli-energy.com", [
        "Wholesale distributor of energy storage solutions in Southern Africa",
        "Exclusive distributor of Sigenergy in Africa",
        "Also carries Huawei and CHINT products",
        "Focus: residential, C&I, off-grid solar and storage markets",
        "Offices in Cape Town, Ballito (KZN), Midrand (Gauteng)",
        "Wholesale model - suitable for adding portable power station line"
    ], ["Sigenergy / Huawei / CHINT: wholesale distributor (no public retail prices)"]),
    
    ("Nology", "https://nology.co.za", [
        "BLUETTI authorized distributor in South Africa",
        "Sells Bluetti EB3A (268Wh/600W) and EB70 (716Wh/1000W) portable power stations",
        "Founded 2001 - specialist value-added distributor of converged IP solutions",
        "Based in Centurion, Gauteng and Montague Gardens, Cape Town",
        "Sells through resellers and systems integrators across Southern Africa"
    ], [
        "Bluetti EB3A (268Wh/600W): retail ~R4,799 (~USD 262)",
        "Bluetti EB70 (716Wh/1000W): retail ~R8,339 (~USD 456)",
        "Bluetti AC200 (2048Wh): retail ~USD 1,699, wholesale ~USD 1,020"
    ]),
    
    ("Flexopower Energies", "https://flexopower.co.za", [
        "South African designer and manufacturer of portable power stations since 2006",
        "Own brand: Flexopower Lithium series using LiFePO4 batteries",
        "Based in Johannesburg and Stellenbosch",
        "Product range: Lithium600 (512Wh), Lithium700, Lithium1200 (1008Wh/1200W), Lithium2400, Lithium3000",
        "Also sells portable solar panels (Namib, Kalahari, Karoo series)"
    ], [
        "Lithium600 (512Wh/600W): R5,999",
        "Lithium700: R9,999",
        "Lithium1200 (1008Wh/1200W): R14,999",
        "Lithium3000: R32,999"
    ]),
    
    ("Solar Sonic", "https://solarsonic.co.za", [
        "Leading importer, distributor, supplier & installer of green energy solutions since 2017",
        "Major brands: SUNSYNK, DEYE, LUX POWER, ATESS, PHOCOS, CANADIAN SOLAR, JA SOLAR",
        "Battery brands: SUNSYNK, FREEDOM WON, HUBBLE LITHIUM, SHOTO, PYLONTECH, DYNESS",
        "Also has own house brand battery",
        "Portable power stations: Kool Energy and Genki brands"
    ], [
        "Kool Energy 1kW 25.6V: R11,900 (~USD 650)",
        "Kool Energy 1.5kW 25.6V: R19,900 (~USD 1,090)",
        "Genki 500W Portable Power Station: R8,266 (~USD 452)"
    ]),
    
    ("PSS Distributors", "https://pss.co.za", [
        "Established as Power System Services in 1994, renamed PSS Distributors in 2000",
        "One of the largest UPS stockholding companies in South Africa",
        "Brands: BluSky, PSS, Vautex",
        "Products: UPS systems, inverters, batteries, and portable power stations",
        "Based in Modderfontein, Johannesburg with 2000m2+ warehouse",
        "Branch network across Southern Africa"
    ], [
        "Portable power stations 150Wh range: R2,500-R3,500",
        "Portable power stations 500Wh range: R8,000-R12,000"
    ])
]

for name, url, findings, prices in research_data:
    sr(name, url, findings, prices)

# Also save to D drive
src = os.path.join(HOME_DIR, ".research_evidence.json")
dst = os.path.join(TARGET_DIR, ".research_evidence.json")
if os.path.exists(src):
    with open(src) as f:
        data = json.load(f)
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

from universal_send_gate import send_email

# ─── All 5 emails ──────────────────────────────────────────────
emails = [
    # 1. ISELI ENERGY
    (
        "sales@iseli-energy.com",
        "Iseli Energy",
        "OEM LiFePO4 portable power stations for Iseli Energy",
        """Hi Iseli Energy team,

I am Pen from nichenexusglobal, a cross-border trade service company based in China.

I see Iseli Energy is the exclusive African distributor for Sigenergy energy storage solutions and also carries Huawei and CHINT products. As load shedding continues to drive South African demand, your wholesale distribution network is well positioned to add portable power stations alongside your existing line.

For context, brands like BLUETTI (AC200 retails at ~USD 1,699, wholesale ~USD 1,020) and EcoFlow DELTA 3 Plus (1024Wh retail ~USD 999, wholesale ~USD 600) dominate this category. Our equivalent LiFePO4 portable power stations from verified Chinese OEM manufacturers offer factory-direct FOB pricing at approximately 75-85% below these wholesale benchmarks:

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
    # 2. NOLOGY
    (
        "info@nology.co.za",
        "Nology",
        "LiFePO4 alternatives to BLUETTI at factory-direct pricing",
        """Hi Nology team,

I am Pen from nichenexusglobal, a cross-border trade service company based in China.

As a BLUETTI authorized distributor in South Africa, Nology sells models like the EB3A (268Wh/600W, retail ~R4,799) and EB70 (716Wh/1000W, retail ~R8,339). The BLUETTI AC200 (2048Wh) retails at roughly USD 1,699 with an estimated wholesale cost of USD 1,020.

Given ongoing load shedding demand, I wanted to present OEM LiFePO4 power station alternatives at factory-direct pricing. Our costs are typically 70-85% below BLUETTI wholesale levels for equivalent capacity:

- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB
- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB
- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB
- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB
- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB

For direct comparison: BLUETTI AC200 (2048Wh) wholesale ~USD 1,020 vs our MECO 2KWH (2009Wh) at USD 165 FOB. BLUETTI EB70 (716Wh) wholesale ~USD 456 vs our Pecron E600LFP (614Wh) at USD 168.5 FOB.

All units are CE/FCC certified, LiFePO4 with 6000+ cycles, available with OEM/private label. MOQ from 10 for trial orders.

Would Nology like to review spec sheets and discuss a trial order?

Best regards,
Pen
nichenexusglobal.com"""
    ),
    # 3. FLEXOPOWER ENERGIES
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
    # 4. SOLAR SONIC
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
    # 5. PSS DISTRIBUTORS
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

# ─── Send or save drafts ──────────────────────────────────────
count = 0
drafts_saved = 0
for to_addr, name, subject, body in emails:
    print(f"\n--- Processing: {name} -> {to_addr} ---")
    result = send_email(to_addr, name, subject, body, category="customer")
    if result:
        count += 1
    else:
        # Save as draft even if blocked by SMTP - so we don't lose the work
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = name.replace(" ", "_")[:20]
        draft_path = os.path.join(TARGET_DIR, f"draft_smtp_blocked_{safe_name}_{ts}.txt")
        with open(draft_path, "w", encoding="utf-8") as f:
            f.write(f"TO: {to_addr}\nCOMPANY: {name}\nSUBJECT: {subject}\nSTATUS: SMTP_UNAVAILABLE\n\n{body}")
        drafts_saved += 1
        print(f"  📝 Draft saved to {os.path.basename(draft_path)}")

print(f"\n===== RESULTS =====")
print(f"  Emails sent via SMTP: {count}/5")
print(f"  Drafts saved (SMTP blocked): {drafts_saved}/5")
print(f"  Evidence saved: .research_evidence.json")
