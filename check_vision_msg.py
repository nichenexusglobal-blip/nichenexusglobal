"""Check Vision Africa's actual messages in full detail"""
import json

with open("C:/nichenexusglobal/whatsapp_messages.jsonl", "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

# Find Vision Africa messages (by LID)
for line in reversed(lines):
    line = line.strip()
    if not line or "196795552559324" not in line:
        continue
    try:
        d = json.loads(line)
    except:
        continue
    
    # Full dump for inspection
    print(json.dumps(d, indent=2, ensure_ascii=False)[:800])
    print("---")
