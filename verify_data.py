#!/usr/bin/env python3
"""Verify key data points from hammer_db for Vision Africa comparison"""
import json

with open("C:/nichenexusglobal/hammer_db.json") as f:
    db = json.load(f)

print("═══ 核验Verifed数据 ═══")
print()

# Check specific verified entries
key_factories = {
    "Anern Energy AN-MPSG-E1200": "1000w",
    "Pecron F1000LFP": "1000w",
    "Pecron E500 LFP": "1000w",
    "PowerLFP LF-B1200PPS": "1000w",
    "PowerLFP LF-B600PPS": "1000w",
    "PowerLFP LF-Y500PPS": "1000w",
    "PowerLFP LF-B2000PPS": "2000w",
    "Pecron E2400 LFP": "2000w",
}

cat_map = {"1000w": "portable_power_1000w", "2000w": "portable_power_2000w"}

for factory_name, cat_key in key_factories.items():
    cat = db.get("categories", {}).get(cat_map[cat_key], {})
    hammers = cat.get("hammers", [])
    found = False
    for h in hammers:
        if h.get("name","") == factory_name:
            found = True
            print(f"✅ {factory_name}")
            print(f"   Wh: {h.get('wh','?')}")
            print(f"   W: {h.get('w','?')}")
            fob = h.get("fob_usd", {})
            if isinstance(fob, dict):
                print(f"   FOB prices: {json.dumps(fob)}")
            else:
                print(f"   FOB: {fob}")
            print(f"   Source: {h.get('source','?')}")
            print(f"   Last updated: {h.get('last_updated','?')}")
            print()
            break
    if not found:
        print(f"❌ {factory_name} NOT FOUND in {cat_key}")
        print()

print()
print("═══ Alibaba报价核验 ═══")
print()

alibaba_entries = [
    ("Shenzhen Taico Technology", "1000w"),
    ("Lansine Intelligent (Zhongshan)", "1000w"),
    ("Jieyang Hangcheng Technology", "1000w"),
    ("Shenzhen Sinorise Info & Tech", "1000w"),
    ("Dongguan Andefeng Battery", "1000w"),
    ("Shenzhen Taico Technology", "2000w"),
    ("Henan Hairongxun New Energy", "2000w"),
]

for factory_name, cat_key in alibaba_entries:
    cat = db.get("categories", {}).get(cat_map[cat_key], {})
    hammers = cat.get("hammers", [])
    for h in hammers:
        if h.get("name","") == factory_name:
            exw = h.get("exw_cny", 0)
            moq = h.get("moq", "?")
            yrs = h.get("years", "?")
            source = h.get("source", "?")
            print(f"✅ {factory_name} ({cat_key})")
            print(f"   EXW: ¥{exw} (USD ${exw/7.2:.0f}) | MOQ: {moq} | Yrs: {yrs}")
            print(f"   Source: {source}")
            print()
            break
