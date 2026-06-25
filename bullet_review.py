#!/usr/bin/env python3
"""Multi-perspective bullet review - run before presenting any draft"""
import json, sys

def review_bullet(company, market, message, channel="whatsapp", is_reply=False, last_client_msg=None):
    """Score from 5 angles. is_reply=True for follow-up messages. 
    last_client_msg: the client's most recent message (for intent matching).
    """
    
    checks = []
    score = 0
    
    # ─── 1. CLIENT视角 ───
    client_issues = []
    if is_reply:
        # For replies: did we answer their question?
        if "$" not in message:
            client_issues.append("没有价格")
        if "?" not in message[-100:]:
            client_issues.append("没有推动对话的问题")
        if len(message) > 500:
            client_issues.append("消息太长")
    else:
        # Original cold outreach checks
        if "I see" not in message and "I noticed" not in message:
            client_issues.append("看不出我们了解他们是谁")
        if "$" not in message:
            client_issues.append("没有价格")
        if "interested" in message.lower() and "?" in message:
            pass
        else:
            client_issues.append("没有清晰的问题/CTA")
        if len(message) > 500:
            client_issues.append("消息太长")
    
    score += 20 if len(client_issues) == 0 else max(0, 20 - 4 * len(client_issues))
    checks.append(("🧑‍💼 客户视角", client_issues, 20))
    
    # ─── 2. SKEPTIC视角 ───
    skeptic_issues = []
    # Does it mention our role correctly?
    if "manufacture" in message.lower() and "sourcing" not in message.lower():
        skeptic_issues.append("说we manufacture=装工厂")
    # Does it have verified numbers?
    if "$" in message:
        price = [w for w in message.split() if "$" in w]
        if price:
            try:
                val = float(price[0].replace("$","").replace(",",""))
                if val > 1000:
                    skeptic_issues.append(f"价格${val}是否核实过?")
            except:
                pass
    # Does it say where we are?
    if "China" not in message and "Shenzhen" not in message:
        skeptic_issues.append("没说我们在中国")
    
    score += 20 if len(skeptic_issues) == 0 else max(0, 20 - 4 * len(skeptic_issues))
    checks.append(("🔍 质疑者视角", skeptic_issues, 20))
    
    # ─── 3. OPERATOR视角 ───
    op_issues = []
    # Can this actually be delivered?
    if channel == "whatsapp" and "+" not in message and "chatId" not in str(sys.argv):
        op_issues.append("WhatsApp号码确认了吗?")
    # Is the tone professional?
    casual_words = ["hey", "man!", "what's up", "how's it going", "gonna", "wanna"]
    for w in casual_words:
        if w in message.lower():
            op_issues.append(f"口语化: {w}")
            break
    # Does it have proper closing?
    if "Best regards" not in message and "Cordialement" not in message and "Salam" not in message:
        op_issues.append("没有适当结尾")
    # Length check
    if len(message) > 600:
        op_issues.append(f"太长({len(message)}字符)")
    
    score += 20 if len(op_issues) == 0 else max(0, 20 - 4 * len(op_issues))
    checks.append(("⚙️ 操盘手视角", op_issues, 20))
    
    # ─── 4. CEO视角（你） ───
    ceo_issues = []
    # Would Pen approve this?
    if "we manufacture" in message.lower():
        ceo_issues.append("装工厂了")
    if "shenzhen" in message.lower() and "China" not in message:
        ceo_issues.append("只写深圳没写中国")
    if "just" in message.lower() and "?" not in message[-20:]:
        ceo_issues.append("语气不够自信")
    
    score += 20 if len(ceo_issues) == 0 else max(0, 20 - 4 * len(ceo_issues))
    checks.append(("👑 CEO视角", ceo_issues, 20))
    
    # ─── 5. 真实意图匹配（对回复消息） ───
    intent_issues = []
    if is_reply and last_client_msg:
        lcm = last_client_msg.lower()
        msg_lower = message.lower()
        
        # 5a: 客户问了价格相关 → 我们的回复有没有提到价格？
        price_keywords = ["price", "cost", "how much", "USD", "$", "cheap", "expensive", "budget", "afford"]
        client_asked_price = any(k in lcm for k in price_keywords)
        our_reply_has_price = "$" in message or "USD" in message
        if client_asked_price and not our_reply_has_price:
            intent_issues.append("客户问价格 → 我们没回价格")
        
        # 5b: 客户问了实力/资质 → 我们的回复有没有回应？
        strength_keywords = ["financial", "base", "capital", "deposit", "pay", "trust", "legit", "scam", "serious"]
        client_asked_strength = any(k in lcm for k in strength_keywords)
        strength_reply_words = ["factory", "verified", "years", "certified", "partner", "quality", "reference", "case", "sample", "trial"]
        our_replied_strength = any(k in msg_lower for k in strength_reply_words)
        if client_asked_strength and not our_replied_strength:
            intent_issues.append("客户质疑实力 → 我们没回应（如financial base）")
        
        # 5c: 客户说中间商/直接找工厂 → 我们有没有解释价值？
        middleman_keywords = ["direct", "middleman", "factory", "manufacturer", "agent", "broker", "intermediary"]
        client_said_middleman = any(k in lcm for k in middleman_keywords)
        value_reply_words = ["compare", "compare", "multiple", "selection", "choose", "best fit", "match", "sourcing"]
        our_explained_value = any(k in msg_lower for k in value_reply_words)
        if client_said_middleman and not our_explained_value:
            intent_issues.append("客户想直找工厂 → 我们没解释通过我们对比的价值")
        
        # 5d: 客户问库存/样品/物流 → 我们的回复有没有回应？
        logistics_keywords = ["stock", "sample", "ship", "delivery", "lead time", "logistics", "warehouse", "freight"]
        client_asked_logistics = any(k in lcm for k in logistics_keywords)
        our_replied_logistics = any(k in msg_lower for k in logistics_keywords)
        if client_asked_logistics and not our_replied_logistics:
            intent_issues.append("客户问物流/样品 → 我们没回")
        
        # 5e: 客户提出具体需求/产品型号 → 我们有没有针对性地回？
        # 这个比较宽松——如果客户说的比较具体，我们的回复也应该具体
        if len(lcm.split()) > 15 and len(msg_lower.split()) < 10:
            intent_issues.append("客户说了很多 → 我们回得太短，没接住")
        
        # 5f: 客户表达不满/犹豫 → 我们有没有接住情绪？
        hesitation_words = ["but", "however", "problem", "concern", "worry", "not sure", "maybe", "difficult"]
        client_hesitated = any(k in lcm for k in hesitation_words)
        acknowledge_words = ["understand", "understand", "yes", "agree", "good point", "fair", "right"]
        we_acknowledged = any(k in msg_lower for k in acknowledge_words)
        if client_hesitated and not we_acknowledged:
            intent_issues.append("客户有顾虑 → 我们没有先表示理解就直接推进")
    
    score += 20 if len(intent_issues) == 0 else max(0, 20 - 4 * len(intent_issues))
    checks.append(("🧠 真实意图匹配", intent_issues, 20))
    
    # ─── RESULTS ───
    print(f"📊 多视角评审: {company} ({market})")
    print(f"   总分: {score}/100  {'🟢' if score >= 90 else '🟡' if score >= 70 else '🔴'}")
    print()
    for role, issues, max_pts in checks:
        pts = max_pts - 5 * len(issues)
        icon = "✅" if not issues else "⚠️"
        print(f"  {role}: {pts}/{max_pts} {icon}")
        for i in issues:
            print(f"    - {i}")
    
    return score >= 80, score, checks

# Test with a sample
if __name__ == "__main__":
    sample = """Hello Dong Solar team,

I am Pen from Nichenexusglobal, a sourcing company based in China. I see you carry EcoFlow power stations in Kenya.

Your RIVER 3 Plus (268Wh) is out of stock. We source LiFePO4 power stations from partner factories. A 1004Wh/500W unit is $165 EXW.

Would this fill the gap in your current lineup?

Best regards,
Pen
Nichenexusglobal"""
    
    ok, score, _ = review_bullet("Dong Solar", "Kenya", sample)
    print(f"\n{'PASS ✅' if ok else 'NEEDS FIX ❌'}")
