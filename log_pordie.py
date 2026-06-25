#!/usr/bin/env python3
"""Log Pordie send"""
import json
from datetime import datetime

with open("C:/nichenexusglobal/send_log.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "email": "info@souoppowerstation.com",
        "company": "SOUOP (Shenzhen Pordie Energy)",
        "subject": "Inquiry: LiFePO4 portable power station catalog & pricing",
        "category": "supplier",
        "success": True
    }, ensure_ascii=False) + "\n")
print("✅ logged")
