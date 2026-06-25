"""Update Pecron record in hammer_db with Nigeria OEM info"""
import json

with open("C:/nichenexusglobal/hammer_db.json", "r") as f:
    db = json.load(f)

# Find Pecron entries
for cat_key, cat in db.get("categories", {}).items():
    hammers = cat.get("hammers", [])
    for h in hammers:
        if "Pecron" in h.get("name", ""):
            if "notes" not in h:
                h["notes"] = ""
            h["notes"] += " | E600LFP has OEM product in Nigeria market (Chris confirmed via WA, Jun 23)"
            print(f"✅ Updated: {h['name']}")

# Also check verified_suppliers
vs = db.get("verified_suppliers", {}).get("hammers", [])
for h in vs:
    if "Pecron" in h.get("name", ""):
        if "notes" not in h:
            h["notes"] = ""
        h["notes"] += " | E600LFP has OEM product in Nigeria market"
        print(f"✅ Updated verified: {h['name']}")

with open("C:/nichenexusglobal/hammer_db.json", "w") as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print("Done")
