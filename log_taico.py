#!/usr/bin/env python3
"""Log Taico send + update hammer DB"""
import json
from datetime import datetime

SEND_LOG = "C:/nichenexusglobal/send_log.jsonl"
HAMMER_DB = "C:/nichenexusglobal/hammer_db.json"

# 1. Log to send_log
entry = {
    "timestamp": datetime.now().isoformat(),
    "email": "sales20@taicopower.com",
    "company": "TAICO Power (TKPW)",
    "subject": "Re: Inquiry: 1000W LiFePO4 Portable Power Station OEM — 200-500 units",
    "category": "supplier",
    "success": True
}
with open(SEND_LOG, "a", encoding="utf-8") as f:
    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
print("✅ send_log updated")

# 2. Update hammer DB status — TAICO Power (TKPW)
with open(HAMMER_DB) as f:
    db = json.load(f)

if "TAICO Power (TKPW)" in db.get("supplier_contacts", {}):
    db["supplier_contacts"]["TAICO Power (TKPW)"]["status"] = "followed_up"
    db["supplier_contacts"]["TAICO Power (TKPW)"]["notes"] = "Replied to Kelly. Asked FOB for A1000+A1000 Pro. Awaiting quote."

# Also update the Shenzhen Taico entry
for entry in db.get("supplier_contacts", {}).values():
    if isinstance(entry, dict) and entry.get("name","") == "Shenzhen Taico Technology":
        entry["status"] = "followed_up"
        entry["notes"] = "已发跟进（回复Kelly回信）。等FOB报价。"

with open(HAMMER_DB, "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)
print("✅ hammer_db status updated")
