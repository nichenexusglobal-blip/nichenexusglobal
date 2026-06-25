"""Add SOUOP/Pordie to hammer database"""
import json

with open("C:/nichenexusglobal/hammer_db.json", "r") as f:
    db = json.load(f)

# Add SOUOP as a verified supplier
souop_entry = {
    "name": "SOUOP / Shenzhen Pordie Energy Technology",
    "source": "verified_email_catalog",
    "contact": "Bella Wang",
    "email": "bella@souoppowerstation.com",
    "whatsapp": "+86 199 7407 9051",
    "since": 2008,
    "employees": "400+",
    "rd_engineers": "40+",
    "products": "350W - 6000W portable power stations",
    "warranty": "3 years",
    "services": "OEM/ODM",
    "sample_moq": "No MOQ for samples",
    "production_base": "Foshan, China",
    "cert_claims": [],
    "data_quality": "A",
    "catalog_pdf": "attachments/supplier_docs/E-brochure of portable power stations from Pordie Energy.pdf",
    "last_updated": "2026-06-24",
    "notes": "Bella replied with catalog. Asked which African markets we serve."
}

# Check if verified_suppliers exists
if "verified_suppliers" not in db:
    db["verified_suppliers"] = {"hammers": []}

vs = db["verified_suppliers"]["hammers"]

# Check if SOUOP already exists
exists = any("SOUOP" in h.get("name", "") for h in vs)
if not exists:
    vs.append(souop_entry)
    db["meta"]["total_hammers"] = db["meta"].get("total_hammers", 0) + 1
    print("✅ Added SOUOP/Pordie to hammer database")
else:
    print("ℹ️ SOUOP already in database")

with open("C:/nichenexusglobal/hammer_db.json", "w") as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f"Total hammers: {db['meta']['total_hammers']}")
