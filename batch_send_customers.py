#!/usr/bin/env python3
"""Batch send 20 customer + 20 supplier emails through universal gate."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/nichenexusglobal"))
from universal_send_gate import send_email

count = 0

# ===== 20 CUSTOMERS (Nails) =====

customers = [
    ("info@ecoflowvietnam.com", "EcoFlow Vietnam", "LiFePO4 power station supply for Vietnam market"),
    ("jackson@truecolourmedia.com", "EcoFlow Malaysia", "LiFePO4 power station supply for Malaysia"),
    ("advertising@mpowergroup.in", "MPower India", "LiFePO4 supply for Indian power backup market"),
    ("info@loomsolar.com", "Loom Solar India", "LiFePO4 power station partnership India"),
    ("info@maryzad.com", "Maryzad Egypt", "LiFePO4 supply for Egyptian solar market"),
    ("info@zadli.com", "Zadli Egypt Saudi", "LiFePO4 power station supply MENA"),
    ("sales@powerpackeg.com", "Power Pack Egypt", "LiFePO4 supply for Egypt"),
    ("info@mea-power.com", "MEA Power Dubai", "LiFePO4 supply for MENA market"),
    ("info@xotechtrading.com", "Xo Tech Trading UAE", "LiFePO4 supply for UAE/GCC"),
    ("cronycrony.group@gmail.com", "eDragon Mall Dubai", "LiFePO4 power station supply Dubai"),
    ("helpdesk@tabbara-electronics.com", "Tabbara Electronics Dubai", "LiFePO4 alternatives for MEA"),
    ("sales@mirage-online.com", "Mirage Indonesia", "LiFePO4 supply for Indonesia"),
    ("sale-ph@bluettipower.com", "BLUETTI Philippines", "LiFePO4 alternative supply Philippines"),
    ("sales@bluettiphilippines.com", "BLUETTI PH", "LiFePO4 supply Philippines"),
    ("info@batteriq.com", "Batteriq Kenya", "LiFePO4 power station supply Kenya"),
    ("sales@shopit.co.ke", "Shopit Kenya", "LiFePO4 supply Kenya"),
    ("sales@phone-x.co.ke", "Phonex Technologies Kenya", "LiFePO4 supply Kenya"),
    ("sales@instok.co.ke", "Instok Kenya", "LiFePO4 supply Kenya"),
    ("sales@grandhub.co.ke", "Grandhub Kenya", "LiFePO4 supply Kenya"),
    ("sales@onsidetechsolutions.co.ke", "Onside Technology Solutions Kenya", "LiFePO4 supply Kenya"),
]

for email_addr, name, subject in customers:
    body = f"""Hi {name.split()[0]} team,

I am Pen from nichenexusglobal, a cross-border trade service company based in China.

I understand {name} distributes portable power solutions. We work with verified Chinese LiFePO4 manufacturers and can offer competitive factory-direct EXW pricing:

- 1000W 1004Wh LiFePO4: EXW USD 145/unit
- 2000W 2009Wh LiFePO4: EXW USD 298/unit
- Both CE/FCC certified, LiFePO4 8000 cycles, OEM/private label available
- MOQ 10 for trial, competitive container pricing for bulk

{name} could potentially save 50-60% vs current supply chain with equivalent LiFePO4 units.

Would you be interested in reviewing spec sheets and discussing a trial order?

Best regards,
Pen
nichenexusglobal.com"""
    
    result = send_email(email_addr, name, subject, body, category="customer")
    if result: count += 1

print(f"\n===== CUSTOMERS SENT: {count}/20 =====")
