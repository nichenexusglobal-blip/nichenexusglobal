"""Check the Pecron WhatsApp message for image content"""
import json

with open("C:/nichenexusglobal/whatsapp_messages.jsonl", "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

for line in reversed(lines):
    if "208950729404658@lid" not in line and "1536147" not in line.lower():
        continue
    
    try:
        d = json.loads(line)
    except:
        continue
    
    print(json.dumps(d, indent=2, ensure_ascii=False)[:1500])
    print("---")
