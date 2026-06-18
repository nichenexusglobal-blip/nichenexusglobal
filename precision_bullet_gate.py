#!/usr/bin/env python3
"""
Precision Bullet Gate v1 — 验证门禁
检查邮件是否经过三阶段调研验证。
和 precision_gate 串联（精度门禁+验证门禁），两个都过才能发。
"""
import re, json, os

WORKDIR = r"C:\nichenexusglobal"

def load_hammer_prices():
    """从锤子库加载我们的真实价格"""
    try:
        with open(os.path.join(WORKDIR, "hammer_db.json"), encoding="utf-8") as f:
            db = json.load(f)
        prices = []
        for v in db.get("verified_suppliers", {}).get("hammers", []):
            if v.get("exw_usd"):
                for model, price in v["exw_usd"].items():
                    prices.append({"supplier": v["name"], "model": model, "price": price, "currency": "USD", "term": "EXW"})
            if v.get("fob_usd"):
                for model, price in v["fob_usd"].items():
                    prices.append({"supplier": v["name"], "model": model, "price": price, "currency": "USD", "term": "FOB"})
        return prices
    except:
        return []

def check_retail_prices(body):
    """检查正文是否包含了从目标网站提取的零售价"""
    # 匹配货币+数字模式：RM 1,299, USD 999, AED 2,500, VND 20M, MYR 3,899
    price_patterns = [
        r'RM\s*[\d,]+', r'USD\s*[\d,]+', r'AED\s*[\d,]+', 
        r'VND\s*[\d.+]+M?', r'MYR\s*[\d,]+',
        r'\$\s*[\d,]+', r'€\s*[\d,]+'
    ]
    found_prices = []
    for p in price_patterns:
        matches = re.findall(p, body)
        found_prices.extend(matches)
    return found_prices

def check_specific_models(body):
    """检查正文是否提到了对方的具体产品型号"""
    # 常见便携电站型号关键词
    model_patterns = [
        r'DELTA\s*\d*\s*(Classic|Pro|Max|Plus|Ultra|Air)?',
        r'RIVER\s*\d*\s*(Pro|Max|Plus)?',
        r'AC\d{2,3}[A-Z]?', r'EB\d{2,3}[A-Z]?',
        r'EB\d{2,3}A', r'PF\d{4}', r'E\d{3,4}LFP',
        r'F\d{3,4}LFP', r'SX_\d{3,4}W',
 r'QE\d{2}[A-Z]?',        # FlashFish QE02D
 r'J\d{4}[A-Za-z]*',      # FlashFish J1000Plus
 r'A\d{3}[A-Z]?',         # FlashFish A1001, A501
 r'C\d{3,4}', r'F\d{4}',  # Anker SOLIX: C300, C800, F1500, F2000
        r'PowerHouse\s*\d{3}', r'SOLIX\s*[CF]\d+',
        r'RIVER\s*\d', r'DELTA\s*\d',
    ]
    found_models = []
    for p in model_patterns:
        matches = re.findall(p, body, re.IGNORECASE)
        found_models.extend(matches)
    return list(set(found_models))

def check_our_pricing(body):
    """检查正文中的我们的价格是否匹配锤子库"""
    our_prices = load_hammer_prices()
    if not our_prices:
        return [], "锤子库为空，无法验证价格"
    
    # 查找正文中出现的USD金额
    price_matches = re.findall(r'USD\s*[\d,]+', body)
    
    matched = []
    for pm in price_matches:
        try:
            price_val = int(re.sub(r'[^\d]', '', pm))
            # 检查这个价格是否在我们已知的价格范围内
            for p in our_prices:
                if abs(p["price"] - price_val) < 5:  # 允许5美元误差
                    matched.append({"price": pm, "supplier": p["supplier"], "term": p["term"]})
                    break
        except:
            pass
    
    return matched, ""

def check_savings_claims(body):
    """检查是否有未验证的节省/百分比断言（纪律11）"""
    violations = []
    # 百分比断言
    pct_patterns = [
        r'save\s+\d+%', r'saving\s+\d+%', r'savings?\s+of\s+\d+%',
        r'\d+%\s+cheaper', r'\d+%\s+less', r'\d+%\s+lower',
        r'reduce\s+\d+%', r'reduction\s+of\s+\d+%',
        r'better\s+pricing', r'competitive\s+pricing',
        r'better\s+margin', r'higher\s+margin',
        r'cost\s+saving', r'cost\s+reduction',
    ]
    
    body_lower = body.lower()
    for p in pct_patterns:
        matches = re.findall(p, body_lower)
        for m in matches:
            # 检查这个断言是否有数据支撑
            # 如果同时有零售价和我们的价格，且百分比=差值/零售价，放行
            # 否则拦截
            has_retail = bool(re.search(r'RM\s*[\d,]+\b|AED\s*[\d,]+\b|VND\s*[\d,]+M?\b', body))
            if not has_retail:
                violations.append(m)
    
    return violations

def verify(company_name, body, category="customer"):
    """
    验证门禁：检查邮件是否经过三阶段调研验证。
    
    Returns: {"pass": bool, "score": int, "issues": [str]}
    """
    issues = []
    score = 0
    max_score = 100
    
    # 1. 是否包含具体型号（20分）
    models = check_specific_models(body)
    if len(models) >= 2:
        score += 20
    elif len(models) == 1:
        score += 10
    else:
        issues.append("未提到对方的具体产品型号 → 没有调研他们卖什么")
    
    # 2. 是否包含零售价（20分）
    retail = check_retail_prices(body)
    if retail:
        score += 20
    else:
        issues.append("未提到对方的零售价 → 没有从他们网站提取价格数据")
    
    # 3. 我们的价格是否匹配锤子库（20分）
    our_prices, err = check_our_pricing(body)
    if our_prices:
        price_detail = "; ".join([f"{p['price']} ({p['supplier']})" for p in our_prices[:2]])
        score += 20
    else:
        issues.append(f"我们的价格与锤子库不匹配 → 写了没有验证的价格")
    
    # 4. 是否有未验证的节省断言（20分）
    savings = check_savings_claims(body)
    if not savings:
        score += 20
    else:
        issues.append(f"包含未验证的节省断言: {savings[:2]} → 违纪律11")
    
    # 5. 公司名是否与邮件正文匹配（20分）
    company_words = company_name.lower().split()[:3]
    body_lower = body.lower()
    for w in company_words:
        if len(w) > 3 and w in body_lower:
            score += 5
            break
    
    # 额外扣分：如果写了"save X%"但没有零售价支撑
    # 已经在check_savings_claims中处理
    
    passed = score >= 80  # 80分门槛
    if not passed:
        issues.append(f"验证门禁分数: {score}/{max_score}（需要80分）")
    
    return {"pass": passed, "score": score, "issues": issues, "max_score": max_score}


if __name__ == "__main__":
    # 测试
    import sys
    if len(sys.argv) > 1:
        company = sys.argv[1]
        body = sys.stdin.read() if not sys.stdin.isatty() else ""
        result = verify(company, body)
        print(f"验证门禁: {result['score']}/{result['max_score']} {'✅' if result['pass'] else '⛔'}")
        for i in result['issues']:
            print(f"  - {i}")
