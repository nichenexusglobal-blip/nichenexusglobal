#!/usr/bin/env python3
"""FACT LIST — Pre-send truth verification.
Every factual statement in an email must trace to a source file.
If a source can't be named → DON'T SEND."""

import json, re, sys, os

# ─── SOURCES DATABASE (grows over time) ──────────
# Format: "claim" → {"source": "file_path", "verified": date}

SOURCES_FILE = "C:/nichenexusglobal/.fact_sources.json"

def load_sources():
    try:
        with open(SOURCES_FILE) as f:
            return json.load(f)
    except:
        return []

def save_source(claim, source_file):
    """Record a verified claim."""
    db = load_sources()
    db.append({
        "claim": claim[:120],
        "source": source_file,
        "verified": "pending" if source_file.startswith("TODO") else "verified"
    })
    with open(SOURCES_FILE, "w") as f:
        json.dump(db, f, indent=2)

# ─── EXTRACT FACTS FROM EMAIL TEXT ──────────────

def extract_facts(text):
    """Find all statements that present as facts."""
    facts = []
    
    # Price claims
    for m in re.finditer(r'[\$£€]\s*[\d,.]+(?:\s*(EXW|FOB|CIF|CFR|DDP))?', text):
        facts.append(("price", m.group().strip()))
    
    # Product specs
    for m in re.finditer(r'(\d+[.,]?\d*)\s*(Wh|W|kWh|kW|V|Ah|kg|cm|mm|inch)', text):
        facts.append(("spec", m.group().strip()))
    
    # "We" statements (about our capability)
    for m in re.finditer(r'We [A-Z][^.]+\.', text):
        facts.append(("we_claim", m.group().strip()))
    
    # "I see / you" statements (about the customer)
    for m in re.finditer(r'(?:I see|I notice|I understand|you sell|you offer|you carry|you distribute|you import|you stock|your company|your website)[^.]*\.', text):
        facts.append(("customer_observation", m.group().strip()))
    
    # Time/business claims
    for m in re.finditer(r'(\d+)\s*(days|weeks|months|years|pcs|units|pieces)', text):
        facts.append(("quantity_timing", m.group().strip()))
    
    return facts


# ═══════════════════════════════════════════════════
# VERIFY
# ═══════════════════════════════════════════════════

def verify_facts(text):
    """Extract and verify every fact in an email."""
    print("=" * 55)
    print("📋 FACT LIST — Every factual statement + its source")
    print("=" * 55)
    
    facts = extract_facts(text)
    
    if not facts:
        print("(no facts extracted — email may be purely conversational)")
        return True
    
    all_ok = True
    
    for ftype, ftext in facts:
        print(f"\n  [{ftype.upper()}] {ftext[:90]}")
        
        # Check local sources database
        sources = load_sources()
        matching = [s for s in sources if s["claim"][:30] in ftext or ftext[:30] in s["claim"]]
        
        if matching:
            for m in matching:
                print(f"    → SOURCE: {m['source']} ({m.get('verified','?')})")
        else:
            # Auto-check common known sources
            found = auto_check_source(ftype, ftext)
            if found:
                print(f"    → SOURCE (auto): {found}")
                save_source(ftext, found)
            else:
                print(f"    ❌ NO SOURCE FOUND")
                all_ok = False
    
    print(f"\n{'='*55}")
    if all_ok:
        print("✅ ALL facts have traceable sources.")
    else:
        print("❌ Some facts have no source. DO NOT SEND.")
        print("   Add sources to .fact_sources.json or remove the claim.")
    print("=" * 55)
    
    return all_ok


def auto_check_source(ftype, ftext):
    """Check if a claim matches known data without needing a prior save."""
    # Check hammer DB prices
    try:
        with open("C:/nichenexusglobal/hammer_db.json") as f:
            hdb = json.load(f)
        for cat_name, cat_data in hdb.get("categories", {}).items():
            for hammer in cat_data.get("hammers", []):
                price = hammer.get("fob_usd", "") or hammer.get("price_range", "") or ""
                if price and f"${price}" in ftext or price.replace("$","") in ftext.replace("$",""):
                    return f"hammer_db.json → {hammer.get('supplier','?')} → {hammer.get('model','?')}"
    except:
        pass
    
    # Check claiming_check.py SOURCES dict
    try:
        from claim_check import SOURCES
        for key, data in SOURCES.items():
            for val in data.values():
                if str(val) in ftext:
                    return f"claim_check.py SOURCES[{key}].{val}"
    except:
        pass
    
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fact_list.py '<email_text>'")
        print("   or:  python fact_list.py --file <path>")
        sys.exit(1)
    
    if sys.argv[1] == "--file":
        with open(sys.argv[2]) as f:
            text = f.read()
    else:
        text = " ".join(sys.argv[1:])
    
    result = verify_facts(text)
    sys.exit(0 if result else 1)
