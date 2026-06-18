#!/usr/bin/env python3
"""Send 5 South Africa cold emails."""
import sys
sys.path.insert(0, "D:/nichenexusglobal")
from universal_send_gate import send_email

emails = []

# 1. Iseli Energy
emails.append(("sales@iseli-energy.com", "Iseli Energy",
    "OEM LiFePO4 portable power stations for Iseli Energy",
    "Hi Iseli Energy team,\n\nI am Pen from nichenexusglobal, a cross-border trade service company based in China.\n\nI see Iseli Energy is the exclusive African distributor for Sigenergy energy storage solutions and also carries Huawei and CHINT products. As load shedding continues to drive South African demand, your wholesale distribution network is well positioned to add portable power stations alongside your existing line.\n\nFor context, brands like BLUETTI (AC200 retails at ~USD 1,699, wholesale ~USD 1,020) and EcoFlow DELTA 3 Plus (1024Wh retail ~USD 999, wholesale ~USD 600) dominate this category. Our equivalent LiFePO4 portable power stations from verified Chinese OEM manufacturers offer factory-direct FOB pricing:\n\n- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB\n- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB\n- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB\n- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB\n- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB\n\nAll units use automotive-grade LiFePO4 cells (6000+ cycles), CE/FCC certified, and support OEM/private label.\n\nWould you be interested in reviewing spec sheets and discussing a trial order?\n\nBest regards,\nPen\nnichenexusglobal.com"))

# 2. Nology
emails.append(("info@nology.co.za", "Nology",
    "LiFePO4 alternatives to BLUETTI at factory-direct pricing",
    "Hi Nology team,\n\nI am Pen from nichenexusglobal, a cross-border trade service company based in China.\n\nAs a BLUETTI authorized distributor in South Africa, Nology sells models like the EB3A (268Wh/600W, retail ~R4,799) and EB70 (716Wh/1000W, retail ~R8,339). The BLUETTI AC200 (2048Wh) retails at roughly USD 1,699 with an estimated wholesale cost of USD 1,020.\n\nGiven ongoing load shedding demand, I wanted to present OEM LiFePO4 power station alternatives at factory-direct pricing.\n\n- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB\n- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB\n- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB\n- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB\n- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB\n\nFor direct comparison: BLUETTI AC200 (2048Wh) wholesale ~USD 1,020 vs our MECO 2KWH (2009Wh) at USD 165 FOB. BLUETTI EB70 (716Wh) wholesale ~USD 456 vs our Pecron E600LFP (614Wh) at USD 168.5 FOB.\n\nAll units are CE/FCC certified, LiFePO4 with 6000+ cycles, available with OEM/private label. MOQ from 10 for trial orders.\n\nWould Nology like to review spec sheets and discuss a trial order?\n\nBest regards,\nPen\nnichenexusglobal.com"))

# 3. Flexopower Energies
emails.append(("info@flexopower.com", "Flexopower Energies",
    "OEM LiFePO4 supply options for Flexopower Energies",
    "Hi Flexopower Energies team,\n\nI am Pen from nichenexusglobal, a cross-border trade service company based in China.\n\nI see Flexopower Energies has been developing portable energy solutions since 2006 with a strong LiFePO4 range: Lithium600 (512Wh at R5,999), Lithium1200 (1008Wh at R14,999), and Lithium3000 (at R32,999). Your engineering-led approach is well respected in the SA camping and load shedding market.\n\nWe offer equivalent quality at factory-direct FOB pricing:\n\n- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB\n- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB\n- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB\n- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB\n- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB\n\nYour Lithium1200 (1008Wh) retails at R14,999 (~USD 820), while our MECO 1KWH (1004Wh, comparable capacity) is USD 145 FOB.\n\nAll units are CE/FCC certified with LiFePO4 6000+ cycles. OEM/private label available. Trial MOQ from 10 units.\n\nWould Flexopower Energies be interested in reviewing spec sheets?\n\nBest regards,\nPen\nnichenexusglobal.com"))

# 4. Solar Sonic
emails.append(("info@solarsonic.co.za", "Solar Sonic",
    "OEM LiFePO4 portable power station supply for Solar Sonic",
    "Hi Solar Sonic team,\n\nI am Pen from nichenexusglobal, a cross-border trade service company based in China.\n\nI see Solar Sonic is a major importer and wholesaler of green energy solutions, carrying SUNSYNK, DEYE, LUX POWER, FREEDOM WON, HUBBLE LITHIUM, and portable stations from Kool Energy (1kW at R11,900, 1.5kW at R19,900) and Genki (500W at R8,266).\n\nWe offer factory-direct LiFePO4 alternatives:\n\n- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB\n- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB\n- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB\n- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB\n- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB\n\nAll units are CE/FCC certified, LiFePO4 with 6000+ cycles, OEM/private label available.\n\nWould Solar Sonic like to review spec sheets for a trial order?\n\nBest regards,\nPen\nnichenexusglobal.com"))

# 5. PSS Distributors
emails.append(("sales@pss.co.za", "PSS Distributors",
    "LiFePO4 portable power stations for PSS Distributors",
    "Hi PSS Distributors team,\n\nI am Pen from nichenexusglobal, a cross-border trade service company based in China.\n\nI see PSS Distributors has been a leading UPS provider in South Africa since 1994, carrying BluSky and PSS brand inverters, Vautex batteries, and portable power stations (150Wh at R2,500-R3,500, 500Wh at R8,000-R12,000). As load shedding continues, the portable power station category is growing fast alongside your traditional UPS business.\n\nWe offer verified Chinese OEM factory-direct LiFePO4 pricing:\n\n- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB\n- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB\n- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB\n- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB\n- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB\n\nAll units are CE/FCC certified, automotive-grade LiFePO4 with 6000+ cycles. OEM/private label available. MOQ from 10 for trial orders.\n\nWould PSS Distributors like to review spec sheets and discuss pricing for a trial order?\n\nBest regards,\nPen\nnichenexusglobal.com"))

for to_addr, name, subject, body in emails:
    try:
        result = send_email(to=to_addr, name=name, subject=subject, body=body, category="customer")
        status = "SENT" if result else "BLOCKED"
        print(f"  {name}: {status}")
    except Exception as e:
        print(f"  {name}: ERROR {str(e)[:80]}")
