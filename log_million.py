#!/usr/bin/env python3
"""Log M Million reply"""
import json
from datetime import datetime

# Log to send_log
with open("C:/nichenexusglobal/send_log.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "channel": "whatsapp",
        "chatId": "2349164337200@s.whatsapp.net",
        "company": "M Million Company",
        "category": "client_reply",
        "success": True
    }, ensure_ascii=False) + "\n")

# Update bullets_db status
with open("C:/nichenexusglobal/bullets_db.json") as f:
    db = json.load(f)
for b in db.get("whatsapp_bullets", []):
    if "million" in b.get("company","").lower():
        b["status"] = "replied"
        b["notes"] = "Replied: Yes LiFePO4, $205 FOB 1280Wh. Answered his 3 questions."
        b["last_reply_date"] = datetime.now().isoformat()
        break
with open("C:/nichenexusglobal/bullets_db.json", "w") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("✅ Logged + bullets_db updated")
