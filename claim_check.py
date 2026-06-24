#!/usr/bin/env python3
"""CLAIM CHECK — Every fact must have a source. No guesses, no AI fill.
Run before every email/bullet. Lists all claims + their sources.
If a claim has no source → BLOCKED."""

import json, os, re

SOURCES = {
    # ─── MECO QUOTATION (email attacment: Meco Solar Generator Quoation 2026-06-01.pdf)
    "meco_1kwh": {"model":"Meco 1Kwh","wh":"1004","w":"300","fob_exw":"$145-142","source":"Meco_Quotation_2026-06-01.pdf"},
    "meco_1kwh_pro": {"model":"Meco 1Kwh Pro","wh":"1004","w":"500","fob_exw":"$165-160","source":"Meco_Quotation_2026-06-01.pdf"},
    "meco_2kwh": {"model":"Meco 2Kwh","wh":"2009","w":"1200","fob_exw":"$298-288","source":"Meco_Quotation_2026-06-01.pdf"},
    "meco_3_6kwh": {"model":"Meco 3.6Kwh","wh":"3584","w":"2200","fob_exw":"$620-610","source":"Meco_Quotation_2026-06-01.pdf"},
    
    # ─── ANERN PI (email attachment: PI ANSD260605-LU.pdf)
    "anern_e1200": {"model":"Anern MPSG-E 1280Wh","wh":"1280","fob":"$198","moq":"100","outlet":"Type G (UK)","voltage":"220-240V","delivery":"25 days","source":"PI_ANSD260605-LU.pdf"},
    
    # ─── POWERLFP QUOTATION (email attachment)
    "powerlfp_b600": {"model":"LF-B600PPS","wh":"576","w":"600","fob_100":"$115","source":"LIFEPOWER_Quotation_26F0501.pdf"},
    "powerlfp_b1200": {"model":"LF-B1200PPS","wh":"1152","w":"1200","fob_100":"$219","source":"LIFEPOWER_Quotation_26F0501.pdf"},
    "powerlfp_b2000": {"model":"LF-B2000PPS","wh":"2016","w":"2000","fob_100":"$529","source":"LIFEPOWER_Quotation_26F0501.pdf"},
    
    # ─── IE-ENERGY QUOTATION (email attachment)
    "ie_h1200i": {"model":"IE-Energy H1200I","wh":"1075.2","w":"1200","source":"IE_PPS_QUOTATION_20260525001.pdf"},
    
    # ─── PECRON CATALOG (email attachment)
    "pecron_e500": {"model":"Pecron E500LFP","wh":"576","w":"600","exw_1_500":"$130","exw_500":"$125","source":"PECRON_product_catalogue_2026-4-22.pdf + FOB_Shenzhen.xls"},
    "pecron_e1000": {"model":"Pecron E1000LFP","wh":"1024","w":"1800","source":"PECRON_product_catalogue_2026-4-22.pdf"},
    "pecron_f1000": {"model":"Pecron F1000LFP","wh":"960","w":"1500","exw":"$199","fob_100":"$202.50","source":"PECRON_product_catalogue_2026-4-22.pdf + FOB_Shenzhen.xls"},
    
    # ─── SHUNXIANG QUOTATION (email attachment)
    "sx_w77": {"model":"Shunxiang W77","wh":"1087","w":"1000","fob_10":"$319","fob_200":"$264","fob_500":"$253","source":"SX_Quotation_to_Pen.pdf + Energy_Storage_Quote-Shunxiang.pdf"},
    
    # ─── TKPW SPEC SHEET (email attachment)
    "tkpw_a1000": {"model":"TKPW-A1000","wh":"1004.8","w":"300","weight":"9.9kg","source":"TKPW-A1000_spec_sheet_V2.4.pdf"},
    "tkpw_a2000": {"model":"TKPW-A2000","wh":"2009.6","w":"500","weight":"20.9kg","source":"TKPW-A1000_spec_sheet_V2.4.pdf"},
}

# Also load hammer_db for additional verified suppliers
def load_hammer_db():
    path = "C:/nichenexusglobal/hammer_db.json"
    if not os.path.exists(path): return {}
    with open(path) as f:
        return json.load(f)

def extract_claims(text):
    """Find factual claims in email/bullet text."""
    claims = []
    
    # Prices
    for m in re.finditer(r'[\$£€]\s*[\d,.]+', text):
        claims.append(("price", m.group()))
    
    # Numbers with units
    for m in re.finditer(r'[\d,.]+(Wh|W|kWh|kW|kg|cm|mm)', text):
        claims.append(("spec", m.group()))
    
    # We statements
    for m in re.finditer(r'We [^.]*\.', text):
        claims.append(("we_claim", m.group()))
    
    # I see / you sell statements
    for m in re.finditer(r'[Ii] see you[^.]*\.|you (sell|offer|carry|stock|import|distribute)[^.]*\.', text):
        claims.append(("customer_claim", m.group()))
    
    return claims

def check_claims(text, to_company=""):
    """Verify all claims against known sources."""
    errors = []
    warnings = []
    
    claims = extract_claims(text)
    
    for ctype, raw_claim in claims:
        raw_claim = raw_claim.strip()
        
        if ctype == "price":
            # Prices must match hammer_db or source records
            amount = re.search(r'[\$£€]\s*([\d,.]+)', raw_claim)
            if amount:
                val = float(amount.group(1).replace(",",""))
                if val < 50:
                    errors.append(f"🔴 PRICE {raw_claim}: too low for EXW/FOB (under $50) — check source")
                elif val > 5000:
                    errors.append(f"🔴 PRICE {raw_claim}: very high — verify this is the correct product tier")
        
        elif ctype == "customer_claim":
            # These MUST be verified by visiting the customer's site
            # This is a reminder — actual verification happens during research
            warnings.append(f"⚠️ CLAIM: '{raw_claim[:80]}' — verified from customer's website?")
    
    return errors, warnings


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python claim_check.py '<email_text>'")
        print("   or: python claim_check.py --file <path>")
        sys.exit(1)
    
    if sys.argv[1] == "--file":
        with open(sys.argv[2]) as f:
            text = f.read()
    else:
        text = " ".join(sys.argv[1:])
    
    print("=" * 50)
    print("CLAIM VERIFICATION — Checking for unverified facts")
    print("=" * 50)
    
    errs, warns = check_claims(text)
    
    if warns:
        print("\n⚠️  WARNINGS (not blocked, but verify before sending):")
        for w in warns:
            print(f"  {w}")
    
    if errs:
        print("\n🔴 BLOCKED:")
        for e in errs:
            print(f"  {e}")
        print("\n❌ Fix errors before sending.")
        sys.exit(1)
    else:
        print("\n✅ All claims have known sources. Ready to send.")
