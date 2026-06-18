#!/usr/bin/env python3
"""Follow-up to Shunxiang Energy — chase EXW/DDP pricing, packing, freight forwarder."""
import sys, os
sys.path.insert(0, r"D:\nichenexusglobal")
os.chdir(r"D:\nichenexusglobal")
from universal_send_gate import send_email

body = """Hi Eason,

I checked your product line on shunxiangenergy.com — you carry 1087Wh Station (W77 at USD 319 FOB), 1450Wh Station (W78 at USD 399 FOB), and 3030Wh Station (W79 NCM at USD 645 FOB). Thanks for the FOB quote PDF.

I also see the 960Wh Battery (F38 LiFePO4) and 3000W Station (F78) on your site — solid range.

A few operational follow-ups for landed cost projections:

1. EXW Dongguan pricing at MOQ 200 and 500 for the W77, W78, W79? This helps compare across your lines.

2. DDP to Rotterdam (Europe) and Los Angeles (US West Coast)?

3. Packing specs — per-unit CBM and gross weight for W77, W78, W79?

4. Forwarder recommendation for sea freight from Shenzhen to SE Asia / Europe?

Also — are the W77 and W78 LiFePO4 or Li-Ion? Your site notes F38 LiFePO4 but F78 and W79 NCM.

For reference — at USD 319 FOB the W77 works out to about USD 0.29/Wh, and at MOQ 500 pricing (USD 253) that drops to USD 0.23/Wh, saving roughly 20% vs single-unit pricing. I'll share the packed specs with buyers once I have the numbers.

Looking forward to your reply with the packing dimensions and EXW pricing — once I have those I can send a trial order to start.

Best regards,
Pen
nichenexusglobal.com"""

result = send_email(
    to='eason@shunxiangenergy.com',
    name='Shunxiang Energy',
    subject='Re: RFQ: 1000W / 2000W LiFePO4 Portable Power Station OEM',
    body=body,
    category='supplier',
    is_reply=True
)
print(f"Result: {result}")
