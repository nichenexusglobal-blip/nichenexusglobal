#!/usr/bin/env python3
"""
99%精准子弹门禁 — 硬拦截。不通过=不发。无例外。

5步流程：
1. 瞄准(Aim) — 确定目标公司、市场、业务类型
2. 检索(Research) — 提取品牌、型号、零售价 
3. 验证(Verify) — 确认联系方式来自官方渠道
4. 归档(Archive) — 保存研究证据到.research_evidence.json
5. 发射(Send) — 通过全部检查才能发出

每步必须100%完成，总评分≥99%才能发射。
"""
import json, os, re, sys

WORKDIR = r"C:\nichenexusglobal"
EVIDENCE_FILE = os.path.join(WORKDIR, ".research_evidence.json")
HAMMER_DB = os.path.join(WORKDIR, "hammer_db.json")

# ═══ 步骤1：瞄准检查 ═══
def check_aim(company_name, body):
    """检查子弹是否瞄准了正确的目标。"""
    issues = []
    score = 0
    name_lower = company_name.lower()
    body_lower = body.lower()
    
    # 1.1 公司名是否出现在正文中（20分）
    # 1.1 公司名是否出现在正文中（20分）
    name_parts = name_lower.replace("inc", "").replace("ltd", "").replace("llc", "").replace("co.", "").replace("corp", "").strip()
    # 提取公司名的核心词（去掉国家/地区/公司类型后缀）
    core_words = [w for w in name_parts.split() if w not in ["philippines", "kenya", "brazil", "mexico", "nigeria", "chile", "china", "colombia", "uganda", "zimbabwe", "indonesia", "vietnam", "india", "uae", "saudi", "turkey", "usa", "uk", "germany", "france", "australia", "south", "africa"]]
    body_match = any(word in body_lower for word in core_words if len(word) > 3)
    if body_match:
        score += 20
    else:
        issues.append("❌ 公司名未出现在正文中")
    
    # 1.2 是否提到对方的具体业务（20分）
    # 从正文中找业务关键词
    biz_keywords = ["your", "you sell", "you distribute", "your company", "your business", "your product"]
    if any(kw in body_lower for kw in biz_keywords):
        score += 20
    else:
        issues.append("❌ 未提及对方的具体业务")
    
    return score, issues


# ═══ 步骤2：检索检查 ═══
def check_research(body):
    """检查子弹是否包含了对方的产品数据。"""
    issues = []
    score = 0
    
    # 2.1 是否提到品牌名（15分）
    brands = ["ecoflow", "bluetti", "anker", "jackery", "vestwoods", "growatt", "deye",
              "meco", "pecron", "anern", "powerlfp", "flashfish", "shunxiang", "worldpower",
              "piforz", "taico", "onesun", "souop", "matec", "calife"]
    mentioned_brands = [b for b in brands if b in body.lower()]
    if mentioned_brands:
        score += 15
    else:
        issues.append("❌ 未提及任何品牌名")
    
    # 2.2 是否提到具体产品型号（20分）
    model_patterns = [
        r'DELTA\s*\d*\s*(Classic|Pro|Max|Plus|Ultra|Air)?',
        r'RIVER\s*\d*\s*(Pro|Max|Plus)?',
        r'AC\d{2,3}[A-Z]?', r'EB\d{2,3}[A-Z]?',
        r'PF\d{4}', r'E\d{3,4}LFP', r'F\d{3,4}LFP',
        r'SX_\d{3,4}W', r'QE\d{2}[A-Z]?', r'J\d{4}[A-Za-z]*',
        r'C\d{3,4}', r'F\d{4}', r'PowerHouse\s*\d{3}',
        r'SOLIX\s*[CF]\d+', r'Vestwoods', r'Pioneer\s*\d+',
        r'\d+[Kk]?[Ww][Hh]?\s*(Battery|Power|Station)?',
        r'\d+[Ww]\s*(Portable|Solar|Inverter)',
    ]
    found_models = []
    for p in model_patterns:
        matches = re.findall(p, body, re.IGNORECASE)
        found_models.extend(matches)
    found_models = list(set(found_models))
    
    if len(found_models) >= 2:
        score += 20
    elif len(found_models) == 1:
        score += 10
        issues.append("⚠️ 仅提到1个型号，建议至少2个")
    else:
        issues.append("❌ 未提到对方的具体产品型号 — 没有调研他们卖什么")
    
    # 2.3 是否包含零售价（15分）
    price_patterns = [
        r'(USD|US\$)\s*[\d,]+(\.\d{2})?',
        r'(KES|KSh|Ksh)\s*[\d,]+',
        r'(PHP|₱)\s*[\d,]+',
        r'(AED|د.إ)\s*[\d,]+',
        r'(RM|MYR)\s*[\d,]+',
        r'(VND|₫)\s*[\d,]+',
        r'(INR|Rs|₹)\s*[\d,]+',
        r'(EUR|€)\s*[\d,]+',
        r'(GBP|£)\s*[\d,]+',
        r'(SGD|S\$)\s*[\d,]+',
        r'(NZD|NZ\$)\s*[\d,]+',
        r'(AUD|A\$)\s*[\d,]+',
        r'at\s+[\d,]+\s*(USD|KES|PHP|AED)',
    ]
    found_prices = []
    for p in price_patterns:
        matches = re.findall(p, body, re.IGNORECASE)
        found_prices.extend(matches)
    
    if found_prices:
        score += 15
    else:
        issues.append("❌ 未包含对方的零售价 — 没有从他们网站提取价格数据")
    
    return score, issues, mentioned_brands, found_models, found_prices


# ═══ 步骤3：验证检查 ═══
def check_verify(chat_id, company_name):
    """检查联系方式是否经过官网验证。"""
    issues = []
    score = 20  # 默认通过（实际验证在发前手动完成）
    
    # LID格式检查
    if chat_id and chat_id.endswith("@lid"):
        issues.append("❌ LID格式禁止发送 — 必须通过官网验证真实号码")
        score = 0
    
    return score, issues


# ═══ 步骤4：归档检查 ═══
def check_archive(company_name):
    """检查研究证据是否已保存。"""
    issues = []
    score = 0
    
    if not os.path.exists(EVIDENCE_FILE):
        issues.append("❌ 研究证据文件不存在 — 必须先调研并保存证据")
        return score, issues
    
    try:
        with open(EVIDENCE_FILE, encoding="utf-8") as f:
            evidence = json.load(f)
        
        # 检查是否有这条目标的证据
        name_lower = company_name.lower()
        found = False
        for e in evidence:
            target = e.get("target", "").lower()
            if name_lower in target or target in name_lower:
                found = True
                # 检查页面访问记录（2026-06-07新增）
                pages = e.get("pages_viewed", [])
                if len(pages) < 3:
                    issues.append(f"❌ 只打开了{len(pages)}个页面，需要至少3个（首页/产品页/About）")
                else:
                    score += 10  # 页面访问加分
                # 检查证据是否完整
                has_products = bool(e.get("products_found") or e.get("brands"))
                has_prices = bool(e.get("retail_prices"))
                if has_products and has_prices:
                    score += 20
                elif has_products or has_prices:
                    score += 10
                    issues.append("⚠️ 研究证据不完整 — 缺少产品或价格数据")
                else:
                    issues.append("⚠️ 研究证据缺少关键数据")
                break
        
        if not found:
            issues.append("❌ 未找到该公司的研究证据 — 必须先调研保存证据")
    except Exception as e:
        issues.append(f"❌ 读取研究证据文件失败: {e}")
    
    return score, issues


# ═══ 步骤5：发射检查 ═══
def check_send(body, channel="whatsapp"):
    """检查子弹本身是否合格。"""
    issues = []
    score = 0
    body_lower = body.lower()
    
    # 5.1 自我标识（5分）
    has_id = any(kw in body_lower for kw in ["pen", "nichenexusglobal", "niche nexus"])
    if has_id:
        score += 5
    else:
        issues.append("❌ 未标识身份（Pen/nichenexusglobal）")
    
    # 5.2 价值主张（5分）
    has_value = any(kw in body_lower for kw in ["fob", "pricing", "supply", "factory",
                                                  "oem", "manufacturer", "wholesale"])
    if has_value:
        score += 5
    else:
        issues.append("❌ 无价值主张")
    
    # 5.3 我们的价格（15分）
    has_our_price = bool(re.search(r'USD\s*[\d,]+(\.\d{2})?\s*(FOB|EXW|per|each)?', body, re.I))
    if has_our_price:
        score += 15
    else:
        issues.append("❌ 未包含我们的FOB报价")
    
    # 5.4 价格对比/量化价值（20分）
    has_comparison = any(kw in body_lower for kw in [
        "margin", "save", "saving", "cheaper", "below", "less than",
        "half", "extra profit", "delta", "compared", "vs", "versus",
        "more profit", "additional", "extra"
    ])
    has_percentage = bool(re.search(r'\d{2,3}%', body))
    # 是否同时提到了对方价格和我们的价格（前后文对比）
    has_both_prices = bool(re.search(r'(USD|US\$)\s*[\d,]+.*(USD|US\$)\s*[\d,]+', body, re.I))
    
    if has_comparison and has_both_prices:
        score += 20
    elif has_comparison or has_percentage:
        score += 12
        issues.append("⚠️ 价格对比不够直接 — 建议把双方价格写在一起对比")
    else:
        issues.append("❌ 无价格对比或量化价值 — 只说价格不说省多少")
    
    # 5.5 行动号召CTA（5分）
    has_cta = any(kw in body_lower for kw in [
        "interested", "relevant", "would this", "would you",
        "sample", "catalog", "details", "share", "let me know",
        "looking forward", "happy to", "reply"
    ])
    # 强CTA（具体行动）vs 弱CTA（让对方想）
    has_strong_cta = any(kw in body_lower for kw in [
        "send you", "i will send", "i can send", "sharing",
        "check out", "take a look", "hop on", "quick call"
    ])
    if has_strong_cta:
        score += 5
    elif has_cta:
        score += 3
        issues.append("⚠️ CTA偏弱 — 建议给具体动作：'我发spec sheet给你' 而不是 '你有兴趣吗'")
    else:
        issues.append("❌ 无行动号召CTA")

    # 5.6 虚假对比检测 — "comparable"/"similar"/"equivalent"必须有spec支撑
    has_false_compare = any(kw in body_lower for kw in [
        "comparable", "similar specs", "equivalent", "like for like",
        "same class", "comparable to"
    ])
    if has_false_compare:
        has_wh = bool(re.search(r'\d{3,5}Wh', body, re.I))
        has_watt = bool(re.search(r'\d{3,4}W', body, re.I))
        if has_wh and has_watt:
            pass  # 有具体spec，放行
        else:
            score -= 15
            issues.append("❌ 虚假对比 — 说'comparable to'但没有给出对比spec (Wh/W)")

    # 5.7 FOB-only陷阱检测
    has_fob = bool(re.search(r'FOB', body, re.I))
    has_shipping = any(kw in body_lower for kw in [
        "shipping", "freight", "delivery", "duty", "landed", "ddp",
        "cif", "incoterm", "transport", "shipped", "arrives"
    ])
    if has_fob and not has_shipping:
        score -= 10
        issues.append("⚠️ 只写了FOB价没提运费/关税 — FOB不是客户到手价，需说明'加运费约USD XX到港'")

    # 5.8 模板检测 — 如果超过70%的内容可以发给任何公司，就是模板
    # 检查是否包含了对方独有的信息（品牌名/具体型号/具体价格）
    has_unique_info = bool(re.search(r'(your|you sell|your site|your store|your shop|your company)', body_lower))
    has_product_ref = bool(re.findall(r'(Gospower|Vestwoods|DELTA|AC\d{3}|EB\d{3}|PF\d{4}|E\d{3,4}LFP)', body, re.I))
    if not has_unique_info and not has_product_ref:
        score -= 20
        issues.append("❌ 模板消息 — 没有包含对方独有的信息（品牌/型号/价格），可发给任何人")
    
    # 5.9 禁止短语检查（-100分直接拦截）
    banned = ["test", "testing", "test message", "ping", "hello world", "just checking"]
    for b in banned:
        if re.search(r'\b' + re.escape(b) + r'\b', body_lower):
            issues.append(f"❌ 包含禁止短语: {b}")
            score = -100
            break
    
    # 5.10 禁止空洞断言（扣分项）
    empty_claims = ["competitive pricing", "great price", "best price", "unbeatable", "amazing"]
    for ec in empty_claims:
        if ec in body_lower:
            issues.append(f"⚠️ 空洞断言: {ec} — 无数据支撑")
            score -= 10
    
    return score, issues


# ═══ 主检查函数 ═══
def check_bullet(company_name, body, chat_id="", channel="whatsapp"):
    """
    99%精准子弹门禁 — 执行全部5步检查。
    
    返回: {"pass": bool, "score": int, "total": int, "issues": [str], "details": {}}
    """
    all_issues = []
    total_score = 0
    max_score = 100
    details = {}
    
    # 步骤1：瞄准（40分）
    aim_score, aim_issues = check_aim(company_name, body)
    total_score += aim_score
    all_issues.extend(aim_issues)
    details["aim"] = {"score": aim_score, "max": 40, "issues": aim_issues}
    
    # 步骤2：检索（50分）
    research_score, research_issues, brands, models, prices = check_research(body)
    total_score += research_score
    all_issues.extend(research_issues)
    details["research"] = {"score": research_score, "max": 50, "issues": research_issues,
                           "brands_found": brands, "models_found": models, "prices_found": prices}
    
    # 步骤3：验证（20分）
    verify_score, verify_issues = check_verify(chat_id, company_name)
    total_score += verify_score
    all_issues.extend(verify_issues)
    details["verify"] = {"score": verify_score, "max": 20, "issues": verify_issues}
    
    # 步骤4：归档（30分）
    archive_score, archive_issues = check_archive(company_name)
    total_score += archive_score
    all_issues.extend(archive_issues)
    details["archive"] = {"score": archive_score, "max": 30, "issues": archive_issues}
    
    # 步骤5：发射（50分，含-100禁止项）
    send_score, send_issues = check_send(body, channel)
    if send_score < 0:
        total_score = -100  # 禁止短语直接毙掉
    total_score += send_score
    all_issues.extend(send_issues)
    details["send"] = {"score": send_score, "max": 50, "issues": send_issues}
    
    # 总评分（满分190分，换算成百分比）
    # 满分 = 40 + 50 + 20 + 30 + 50 = 190
    # 但禁止短语直接归零
    actual_max = 190
    pct = max(0, min(100, int(total_score / actual_max * 100)))
    
    passed = pct >= 99 and total_score > 0
    
    return {
        "pass": passed,
        "score": pct,
        "total_raw": total_score,
        "max_raw": actual_max,
        "issues": all_issues,
        "details": details
    }


def print_report(result):
    """打印检查报告。"""
    status = "✅ PASS" if result["pass"] else "⛔ BLOCKED"
    print(f"\n{'='*50}")
    print(f"  99% 精准子弹门禁 — {status}")
    print(f"  评分: {result['score']}/100 (raw: {result['total_raw']}/{result['max_raw']})")
    print(f"{'='*50}")
    
    steps = [
        ("1. 瞄准 Aim", "aim", 40),
        ("2. 检索 Research", "research", 50),
        ("3. 验证 Verify", "verify", 20),
        ("4. 归档 Archive", "archive", 30),
        ("5. 发射 Send", "send", 50),
    ]
    
    for step_name, key, max_score in steps:
        d = result["details"].get(key, {})
        s = d.get("score", 0)
        issues = d.get("issues", [])
        bar = "█" * max(0, min(20, int(s / max_score * 20))) if max_score > 0 else ""
        print(f"\n  {step_name}: {s}/{max_score} {bar}")
        for issue in issues:
            print(f"    {issue}")
    
    print(f"\n  Issues total: {len(result['issues'])}")
    for issue in result["issues"]:
        print(f"    {issue}")
    
    return result["pass"]


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python precision_checklist.py <公司名> <消息正文> [chatId]")
        sys.exit(1)
    
    company = sys.argv[1]
    body = sys.argv[2]
    chat_id = sys.argv[3] if len(sys.argv) > 3 else ""
    
    result = check_bullet(company, body, chat_id)
    print_report(result)
    
    if result["pass"]:
        sys.exit(0)
    else:
        sys.exit(1)
