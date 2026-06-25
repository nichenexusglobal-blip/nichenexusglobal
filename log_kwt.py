#!/usr/bin/env python3
"""Log KWT send"""
import json
from datetime import datetime
with open("C:/nichenexusglobal/send_log.jsonl", "a") as f:
    f.write(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "email": "sales@kwttechmart.com",
        "company": "KWT Tech Mart (Uganda)",
        "subject": "Portable power station 1280Wh LiFePO4 — following up on our WhatsApp chat",
        "category": "customer",
        "success": True
    }, ensure_ascii=False) + "\n")
print("✅ logged")
