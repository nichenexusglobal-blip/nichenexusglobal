#!/usr/bin/env python3
"""
Hammer DB — 锤子数据库查询工具

用法:
  python hammer_db.py                     列出所有品类
  python hammer_db.py portable_power_1000w  列出该品类锤子排行榜
  python hammer_db.py --best portable_power_1000w  推荐最优锤子
  python hammer_db.py --best portable_power_2000w  推荐最优锤子
  python hammer_db.py --compare pecorn piforz  对比两个供应商
  python hammer_db.py --vs 2048Wh         查出2048Wh品类的我们价格vs竞争对手
"""

import json, sys, os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hammer_db.json")

def load():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def list_categories(db):
    print("锤子数据库 — 品类列表")
    print("=" * 50)
    for cat_id, cat in db["categories"].items():
        h = len(cat.get("hammers", []))
        v = sum(1 for s in cat.get("hammers", []) if s.get("status","") == "verified_quote")
        print(f"  {cat_id}: {cat['name']} ({h}个锤子, {v}已验证)")

def show_category(db, cat_id):
    cat = db["categories"].get(cat_id) or db.get(cat_id)
    if not cat:
        print(f"品类 {cat_id} 不存在")
        return
    print(f"\n{cat['name']}")
    print(f"市场价范围: ¥{cat['market_price_cny_range']['min']} - ¥{cat['market_price_cny_range']['max']}")
    print(f"FOB基准: ${cat['benchmark_fob_usd']['low']} - ${cat['benchmark_fob_usd']['high']}")
    print(f"\n排名 | 供应商 | 年限 | EXW(¥) | MOQ | 评分 | 来源")
    print("-" * 70)
    for h in sorted(cat.get("hammers", []), key=lambda x: x.get("score", 0), reverse=True):
        r = h.get("alibaba_rating", "N/A")
        s = h.get("score", "?")
        status = "✓" if h.get("status") == "verified_quote" else "○" if h.get("status") == "unverified_quote" else "·"
        print(f"  #{h['rank']:<3} | {h['name'][:25]:<25} | {h.get('years','?'):>2}yr | ¥{h.get('exw_cny','?'):<8} | {h.get('moq','?'):<5} | {s} | {status}")
    print()
    print("图例: ✓=已验证报价  ○=列表页价待验证  ·=其他")

def best_hammer(db, cat_id):
    cat = db["categories"].get(cat_id)
    if not cat:
        print(f"品类 {cat_id} 不存在"); return
    hammers = sorted(cat.get("hammers", []), key=lambda x: x.get("score", 0), reverse=True)
    if not hammers:
        print("该品类暂无锤子"); return
    best = hammers[0]
    print(f"\n🥇 最优锤子 — {cat['name']}")
    print(f"  供应商: {best['name']} ({best.get('years','?')}年)")
    print(f"  价格: ¥{best.get('exw_cny','?')} EXW (≈${best.get('exw_cny',0)/7.2:.0f} USD)")
    print(f"  MOQ: {best.get('moq','?')}")
    print(f"  评分: {best.get('score','?')}/100")
    print(f"  来源: {best.get('source','?')}")
    print(f"  状态: {best.get('status','?')}")
    if best.get("notes"):
        print(f"  备注: {best['notes']}")

def compare_vs_competitor(db, capacity_wh):
    """对比我们供应商价格 vs 竞争对手品牌价格"""
    comp = db.get("competitor_brands", {}).get("brands", [])
    matching = [b for b in comp if abs(b.get("capacity_wh", 0) - capacity_wh) < 300]
    if not matching:
        print(f"未找到容量约{capacity_wh}Wh的竞争对手数据"); return
    
    print(f"\n📊 价格对比 — ~{capacity_wh}Wh LiFePO4")
    print(f"{'对手品牌':<20} {'零售价':<12} {'批发价':<12} {'我们FOB':<12} {'优势':<12}")
    print("-" * 72)
    
    # Estimate our FOB from category data
    for cat_id, cat in db["categories"].items():
        ranges = {"1000": (800, 1024), "2000": (1500, 2500)}
        for k, (lo, hi) in ranges.items():
            if lo <= capacity_wh <= hi:
                our_fob = cat["benchmark_fob_usd"]["mid"]
                for b in matching:
                    saving = b.get("est_wholesale_usd", 0) - our_fob
                    saving_pct = int(saving / b.get("est_wholesale_usd", 1) * 100)
                    print(f"{b['name']+' '+b.get('model',''):<20} ${b.get('retail_usd',0):<8}  ${b.get('est_wholesale_usd',0):<8}  ${our_fob:<8}  ${saving:<8}(-{saving_pct}%)")
                return
    print("  无法估算我们的FOB价(品类未收录)")

if __name__ == "__main__":
    db = load()
    if len(sys.argv) == 1:
        list_categories(db)
    elif sys.argv[1] == "--best" and len(sys.argv) > 2:
        best_hammer(db, sys.argv[2])
    elif sys.argv[1] == "--vs" and len(sys.argv) > 2:
        compare_vs_competitor(db, int(sys.argv[2]))
    else:
        show_category(db, sys.argv[1])
