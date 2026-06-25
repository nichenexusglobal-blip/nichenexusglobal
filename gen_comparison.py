#!/usr/bin/env python3
"""Generate factory comparison table from hammer_db.json — robust version"""
import json

with open("C:/nichenexusglobal/hammer_db.json") as f:
    db = json.load(f)

rate = 7.2

def fmt_fob(fob):
    if not fob or not isinstance(fob, dict):
        return "?"
    # Try various FOB price keys
    for key in ["fob_10", "fob_100", "exw_500", "fob"]:
        v = fob.get(key)
        if v:
            return f"${v}"
    return "?"

for cat_key in ["portable_power_1000w", "portable_power_2000w"]:
    cat = db.get("categories", {}).get(cat_key, {})
    if not cat:
        continue
    
    print(f"{'='*80}")
    print(f"  {cat['name']}")
    print(f"  Market range: CNY {cat['market_price_cny_range']['min']}-{cat['market_price_cny_range']['max']}")
    print(f"  FOB benchmark: ${cat['benchmark_fob_usd']['low']}-${cat['benchmark_fob_usd']['high']}")
    print(f"{'='*80}")
    print()
    
    hammers = cat.get("hammers", [])
    verified = [h for h in hammers if h.get("source","").startswith("verified")]
    unverified = [h for h in hammers if not h.get("source","").startswith("verified")]
    
    print("  📄 VERIFIED (with spec sheets / PI):")
    print(f"  {'Factory':<28} {'Wh':<8} {'W':<6} {'Price':<12} {'Cert':<12}")
    print(f"  {'-'*66}")
    for h in verified:
        name = h.get("name","?")[:27]
        wh = h.get("wh",0) or ""
        w = h.get("w",0) or ""
        fob = fmt_fob(h.get("fob_usd",{}))
        cert = h.get("cert","") or h.get("cert_claims",[])
        if isinstance(cert, list):
            cert = ", ".join(cert) if cert else "-"
        print(f"  {name:<28} {str(wh):<8} {str(w):<6} {fob:<12} {cert:<12}")
    
    print()
    print("  🔍 ALIBABA LISTINGS (unverified):")
    print(f"  {'Factory':<28} {'EXW(CNY)':<12} {'EXW(USD)':<10} {'MOQ':<6} {'Yrs':<5} {'Rating':<8}")
    print(f"  {'-'*69}")
    for h in unverified:
        name = h.get("name","?")[:27]
        exw = h.get("exw_cny",0)
        if not exw:
            continue
        usd = round(exw / rate, 0)
        moq = str(h.get("moq","?"))
        yrs = str(h.get("years","?"))
        rating = str(h.get("alibaba_rating","-"))
        print(f"  {name:<28} ¥{exw:<9} ${usd:<7.0f} {moq:<6} {yrs:<5} {rating:<8}")
    
    print()
