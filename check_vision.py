#!/usr/bin/env python3
"""Review Vision Africa draft"""
import sys
sys.path.insert(0, "C:/nichenexusglobal")
from bullet_review import review_bullet

msg = """Thank you for your reply. It's great to hear you own the TO-GO power station brand and are looking to expand in the Nigerian market.

We work on an order-based model: you place an order, we handle production and logistics from our partner factories in China. No upfront inventory required on your end.

A 1004Wh/500W LiFePO4 unit is $165 EXW. Would you like me to send the spec sheet and product photos?

Best regards,
Pen
Nichenexusglobal"""

ok, score, checks = review_bullet("Vision Africa", "Nigeria", msg, is_reply=True)
print(f"\n{'PASS ✅' if ok else 'NEEDS FIX ❌'} -- Score: {score}/100")
