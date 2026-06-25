#!/usr/bin/env python3
"""Full audit of hammer_db.json - what's complete, what's missing"""
import json, os

with open("C:/nichenexusglobal/hammer_db.json") as f:
    db = json.load(f)

rate = 7.2

print("══════════════════════════════════════════════════")
print("  锤子库全面审计")
print("══════════════════════════════════════════════════")
print()

# Category overview
cats = db.get("categories", {})
print(f"分类数: {len(cats)}")
total_entries = 0
for cat_key, cat in cats.items():
    hammers = cat.get("hammers", []) if isinstance(cat, dict) else []
    if isinstance(hammers, dict):
        entries = len(hammers)
    elif isinstance(hammers, list):
        entries = len(hammers)
    else:
        entries = 0
    total_entries += entries
    print(f"  {cat_key}: {entries} entries")
print(f"  总计: {total_entries}")
print()

# Per-category detailed audit
for cat_key in ["portable_power_1000w", "portable_power_2000w"]:
    cat = cats.get(cat_key, {})
    if not cat:
        continue
    
    print(f"{'='*80}")
    print(f"  🔨 {cat.get('name', cat_key)}")
    print(f"{'='*80}")
    
    hammers = cat.get("hammers", [])
    
    # Count by status
    verified = [h for h in hammers if str(h.get("source","")).startswith("verified")]
    unverified = [h for h in hammers if not str(h.get("source","")).startswith("verified")]
    
    print(f"  已验证: {len(verified)} | 待验证(阿里): {len(unverified)}")
    print()
    
    # Verified entries - check for missing FOB
    print("  📄 已验证条目——FOB价格完整性：")
    for h in verified:
        name = h.get("name","?")
        fob = h.get("fob_usd", {})
        has_fob = bool(fob and isinstance(fob, dict) and any(v for v in fob.values() if v))
        wh = h.get("wh", "?")
        contact = h.get("contact","?") or h.get("contact_person","?")
        email = h.get("email","?")[:30]
        status = "✅ 有FOB价" if has_fob else "⚠️ FOB为空"
        print(f"    {status} | {name[:30]:<30} | Wh:{str(wh):<8} | {contact:<15} | {email}")
    
    print()
    
    # Market coverage analysis
    print("  📊 市场覆盖面：")
    wh_range = [h.get("wh",0) or 0 for h in hammers]
    w_range = [h.get("w",0) or 0 for h in hammers]
    if wh_range:
        print(f"    Wh范围: {min(wh_range)}-{max(wh_range)}")
    if w_range:
        print(f"    W范围: {min(w_range)}-{max(w_range)}")
    
    # Price range by verified entries
    verified_prices = []
    for h in verified:
        fob = h.get("fob_usd", {})
        if isinstance(fob, dict):
            for k, v in fob.items():
                if v and isinstance(v, (int, float)):
                    verified_prices.append((h["name"], k, v, h.get("wh",0)))
    
    if verified_prices:
        min_price = min(p[2] for p in verified_prices)
        max_price = max(p[2] for p in verified_prices)
        print(f"    已验证FOB价范围: ${min_price}-${max_price}")
        print(f"    可用报价点数: {len(verified_prices)}")
    
    print()
    
    # Unverified - check completeness
    print("  🔍 待验证(阿里)条目——数据完整性：")
    for h in unverified:
        name = h.get("name","?")
        exw = h.get("exw_cny", 0)
        moq = h.get("moq", "?")
        yrs = h.get("years", "?")
        rating = h.get("alibaba_rating", "?")
        certs = h.get("cert_claims", [])
        has_cert = bool(certs)
        usd = round(exw / rate, 0) if exw else 0
        print(f"    {name[:30]:<30} EXW:¥{exw:<6}(${usd:<3.0f}) MOQ:{str(moq):<4} {yrs}年 {'✅认证' if has_cert else '❌无认证'}")
    
    print()

# Competitor brands analysis
comp = cats.get("competitor_brands", {})
if comp:
    print(f"{'='*80}")
    print(f"  🔍 Competitor Brands ({len(comp)} entries)")
    print(f"{'='*80}")
    if isinstance(comp, dict):
        for k, v in comp.items():
            if k != "hammers":
                print(f"    {k}: {str(v)[:80]}")
    print()

# Identify specific gaps
print(f"{'='*80}")
print("  🎯 缺口分析 & 待办")
print(f"{'='*80}")
print()
print("  ✅ 可立即使用的（有FOB价）：")
for cat_key in ["portable_power_1000w", "portable_power_2000w"]:
    cat = cats.get(cat_key, {})
    hammers = cat.get("hammers", [])
    for h in hammers:
        fob = h.get("fob_usd", {})
        if isinstance(fob, dict) and any(v for v in fob.values() if v):
            name = h.get("name","?")
            wh = h.get("wh",0)
            # Skip Pecron if Nigeria restriction
            notes = h.get("notes","")
            restricted = "Nigeria" in notes or "West Africa" in notes
            print(f"    {'⚠️ ' if restricted else '✅ '} {name} | {wh}Wh | FOB: {json.dumps(fob)} {'(尼日利亚不可用)' if restricted else ''}")

print()
print("  ⚠️ 需跟进（有规格书没FOB价）：")
for cat_key in ["portable_power_1000w", "portable_power_2000w"]:
    cat = cats.get(cat_key, {})
    hammers = cat.get("hammers", [])
    for h in hammers:
        source = h.get("source","")
        fob = h.get("fob_usd", {})
        has_fob = isinstance(fob, dict) and any(v for v in fob.values() if v)
        if source.startswith("verified") and not has_fob:
            name = h.get("name","?")
            contact = h.get("contact","?")
            email = h.get("email","?")[:30]
            print(f"    {name:<35} 联系人:{contact:<15} {email}")

print()
print("  🔍 阿里报价→验证优先级（价格好+公司靠谱的）：")
for cat_key in ["portable_power_1000w", "portable_power_2000w"]:
    cat = cats.get(cat_key, {})
    hammers = cat.get("hammers", [])
    scored = []
    for h in hammers:
        if not h.get("source","").startswith("verified"):
            exw = h.get("exw_cny", 0)
            yrs = h.get("years", 0) or 0
            rating = h.get("alibaba_rating", 0) or 0
            reviews = h.get("alibaba_reviews", 0) or 0
            moq = h.get("moq", 100) or 100
            # Simple score: price attractiveness + trust
            if exw and yrs >= 3 and moq <= 10:
                scored.append((exw, -yrs, h.get("name","?"), moq))
    for exw, _, name, moq in sorted(scored)[:5]:
        print(f"    {name:<35} EXW:¥{exw}(${exw/rate:.0f}) MOQ:{moq}")
