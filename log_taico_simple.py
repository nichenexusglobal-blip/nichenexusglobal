#!/usr/bin/env python3
"""Log Taico email send to send_log"""
import json
from datetime import datetime

with open("C:/nichenexusglobal/send_log.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "email": "sales20@taicopower.com",
        "company": "TAICO Power (TKPW)",
        "subject": "Re: Inquiry: 1000W LiFePO4 Portable Power Station OEM — 200-500 units",
        "category": "supplier",
        "success": True
    }, ensure_ascii=False) + "\n")
print("✅ logged")
