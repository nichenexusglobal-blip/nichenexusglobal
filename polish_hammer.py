#!/usr/bin/env python3
"""Polish hammer database - standardize format, add $/Wh, organize by segment"""
import json

WORKDIR = "C:/nichenexusglobal"
with open(f"{WORKDIR}/hammer_db.json") as f:
    db = json.load(f)

hammers = db.get("verified_suppliers", {}).get("hammers", [])

def grade_str(g):
    """Normalize grade to string"""
    if isinstance(g, dict):
        return g.get("grade", "C")
    return str(g) if g else "C"

def label(grade):
    labels = {"A": "VERIFIED - PDF/email pricing confirmed",
              "B": "PARTIAL - some data confirmed",
              "C": "LIMITED - catalog info, no pricing",
              "D": "SUSPICIOUS - unverified source"}
    return labels.get(grade, "UNKNOWN")

# Standardize all hammers
for h in hammers:
    g = grade_str(h.get("data_quality", "C"))
    h["data_quality"] = g
    h["data_quality_label"] = label(g)
    
    # Remove old format fields
    h.pop("grade", None)
    
    # Calculate $/Wh for each product
    prods = h.get("products", [])
    for p in prods:
        wh = p.get("wh", 0)
        if wh > 0:
            # Find best price
            price = p.get("price", 0) or p.get("fob_10", 0) or p.get("exw_10_49", 0)
            if price > 0:
                p["usd_per_wh"] = round(price / wh, 3)
    
    # Market segmentation
    if prods:
        max_wh = max(p.get("wh", 0) for p in prods)
        if max_wh <= 600:
            h["market_segment"] = "mini (under 600Wh)"
        elif max_wh <= 1500:
            h["market_segment"] = "portable (600-1500Wh)"
        elif max_wh <= 4000:
            h["market_segment"] = "mid-size (1500-4000Wh)"
        else:
            h["market_segment"] = "large (4000Wh+)"

# Sort: A grade first, then by name
hammers.sort(key=lambda h: (h.get("data_quality", "Z"), h.get("name", "")))

db["verified_suppliers"]["hammers"] = hammers

with open(f"{WORKDIR}/hammer_db.json", "w") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

# Summary
print("HAMMER DB STATUS")
print("=" * 60)
for h in hammers:
    g = h.get("data_quality", "?")
    name = h.get("name", "")
    seg = h.get("market_segment", "unclassified")
    prods = len(h.get("products", []))
    imgs = h.get("image_count", 0)
    best = ""
    for p in h.get("products", []):
        if p.get("usd_per_wh"):
            best = f" best ${p['usd_per_wh']:.2f}/Wh"
            break
    print(f"  [{g}] {name:25s} {seg:25s} {prods} prods, {imgs} imgs{best}")

total_products = sum(len(h.get("products", [])) for h in hammers)
print(f"\nTotal: {len(hammers)} suppliers, {total_products} products")
