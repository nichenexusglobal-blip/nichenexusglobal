#!/usr/bin/env python3
"""Send 5 UAE/Nigeria cold emails."""
import sys, os
# Unset proxy env vars for SMTP
for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    os.environ.pop(k, None)

sys.path.insert(0, "D:/nichenexusglobal")
from universal_send_gate import send_email

emails = []

# 1. XO Tech Trading (UAE)
emails.append(("info@xotechtrading.com", "XO Tech Trading",
    "LiFePO4 portable power station supply for XO Tech Trading",
    "Hi XO Tech Trading team,\n\nI am Pen from nichenexusglobal, a cross-border trade service company based in China.\n\nI see XO Tech Trading is a well-established wholesale electronics distributor in Dubai supplying top brands like Apple, Samsung, JBL, Bose, Sony, Xiaomi, and Starlink to retailers and resellers. Your current lineup of power banks, chargers, and consumer electronics positions you well to add portable power stations as a complementary category.\n\nBrands like EcoFlow (DELTA 2 retails at ~USD 999) and BLUETTI (AC200 retails at ~USD 1,699) dominate the portable power station market. Our equivalent LiFePO4 portable power stations from verified Chinese OEM manufacturers offer factory-direct FOB pricing:\n\n- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB\n- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB\n- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB\n- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB\n- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB\n\nAll units use automotive-grade LiFePO4 cells (6000+ cycles), CE/FCC certified, and support OEM/private label.\n\nWould XO Tech Trading like to review spec sheets and discuss a trial order?\n\nBest regards,\nPen\nnichenexusglobal.com"))

# 2. ADEX International (UAE)
emails.append(("info@adexuae.com", "ADEX International",
    "OEM LiFePO4 portable power station supply for ADEX International",
    "Hi ADEX International team,\n\nI am Pen from nichenexusglobal, a cross-border trade service company based in China.\n\nI see ADEX International is an industrial machinery and equipment supplier based in Dubai, UAE. As backup power demand continues to grow across the UAE and wider Middle East market, portable power stations represent a strong complementary category to your existing industrial equipment line.\n\nFor context, brands like EcoFlow (DELTA 2 retails at ~USD 999) and BLUETTI (AC200 retails at ~USD 1,699) dominate this category. Our equivalent LiFePO4 portable power stations from verified Chinese OEM manufacturers offer factory-direct FOB pricing:\n\n- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB\n- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB\n- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB\n- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB\n- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB\n\nAll units are CE/FCC certified, LiFePO4 with 6000+ cycles, and available with OEM/private label. MOQ from 10 units for trial orders.\n\nWould ADEX International like to review spec sheets?\n\nBest regards,\nPen\nnichenexusglobal.com"))

# 3. MEA Power (UAE)
emails.append(("info@mea-power.com", "MEA Power",
    "OEM LiFePO4 portable power station supply for MEA Power",
    "Hi MEA Power team,\n\nI am Pen from nichenexusglobal, a cross-border trade service company based in China.\n\nI see MEA Power is an authorized distributor of solar systems and lithium batteries based in Jebel Ali, Dubai. Your existing presence in premium renewable energy solutions makes you a natural fit for portable power stations — a rapidly growing category in the UAE and Middle East.\n\nFor context, brands like EcoFlow (DELTA 2 retails at ~USD 999, EcoFlow DELTA Pro at ~USD 3,699) and BLUETTI (AC200 retails at ~USD 1,699) dominate this category. Our equivalent LiFePO4 portable power stations from verified Chinese OEM manufacturers offer factory-direct FOB pricing:\n\n- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB\n- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB\n- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB\n- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB\n- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB\n\nAll units are CE/FCC certified, automotive-grade LiFePO4 with 6000+ cycles, and available with OEM/private label. MOQ from 10 units.\n\nWould MEA Power like to review spec sheets?\n\nBest regards,\nPen\nnichenexusglobal.com"))

# 4. TD Africa (Nigeria, EcoFlow)
emails.append(("chioma@tdafrica.com", "TD Africa",
    "OEM LiFePO4 portable power station alternatives for TD Africa",
    "Hi Chioma and the TD Africa team,\n\nI am Pen from nichenexusglobal, a cross-border trade service company based in China.\n\nI see TD Africa is the leading technology distribution company in Sub-Saharan Africa and an authorized EcoFlow distributor in Nigeria. Your portfolio includes EcoFlow portable power stations alongside HP, Dell, Lenovo, and Microsoft products.\n\nFor reference, EcoFlow DELTA 2 (1024Wh) retails at approximately USD 999, and the DELTA Pro (3600Wh) at approximately USD 3,699. Our equivalent LiFePO4 portable power stations from verified Chinese OEM manufacturers offer factory-direct FOB pricing as an alternative or private-label line:\n\n- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB\n- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB\n- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB\n- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB\n- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB\n\nAll units use automotive-grade LiFePO4 cells (6000+ cycles), CE/FCC certified, and support OEM/private label.\n\nWould TD Africa like to review spec sheets and discuss a trial order?\n\nBest regards,\nPen\nnichenexusglobal.com"))

# 5. Detopsy Electrical Shop (Nigeria)
emails.append(("info@detopsyelectricalshop.com", "Detopsy Electrical Shop",
    "OEM LiFePO4 portable power station supply for Detopsy Electrical Shop",
    "Hi Detopsy Electrical Shop team,\n\nI am Pen from nichenexusglobal, a cross-border trade service company based in China.\n\nI see Detopsy Electrical Shop is a leading electrical supplies retailer in Port Harcourt, Nigeria, selling EcoFlow portable power stations, BLUETTI power stations, ABB, Schneider Electric, and APC UPS systems. Your existing EcoFlow and BLUETTI portable power station offerings show strong demand in the Nigerian backup power market.\n\nFor reference, EcoFlow DELTA 2 (1024Wh) retails at approximately USD 999, and BLUETTI AC200 (2048Wh) retails at approximately USD 1,699. Our equivalent LiFePO4 portable power stations from verified Chinese OEM manufacturers offer factory-direct FOB pricing:\n\n- MECO 1KWH (1004Wh LiFePO4): USD 145/unit FOB\n- MECO 2KWH (2009Wh LiFePO4): USD 165/unit FOB\n- Anern 1280Wh (1200W LiFePO4): USD 205/unit FOB\n- Pecron E600LFP (614Wh LiFePO4): USD 168.5/unit FOB\n- PowerLFP LF-B1200PPS (1152Wh LiFePO4): USD 219/unit FOB\n\nAll units are CE/FCC certified, automotive-grade LiFePO4 with 6000+ cycles, and available with OEM/private label.\n\nWould Detopsy Electrical Shop like to review spec sheets?\n\nBest regards,\nPen\nnichenexusglobal.com"))


for to_addr, name, subject, body in emails:
    try:
        result = send_email(to=to_addr, name=name, subject=subject, body=body, category="customer")
        status = "SENT" if result else "BLOCKED"
        print(f"  {name}: {status}")
    except Exception as e:
        print(f"  {name}: ERROR {str(e)[:80]}")
