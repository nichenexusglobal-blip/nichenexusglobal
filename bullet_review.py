#!/usr/bin/env python3
"""Multi-perspective bullet review - run before presenting any draft"""
import json, sys

def review_bullet(company, market, message, channel="whatsapp", is_reply=False):
    """Score from 4 angles. is_reply=True for follow-up messages."""
    
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
    
    score += 25 if len(client_issues) == 0 else max(0, 25 - 5 * len(client_issues))
    checks.append(("🧑‍💼 客户视角", client_issues, 25))
    
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
    
    score += 25 if len(skeptic_issues) == 0 else max(0, 25 - 5 * len(skeptic_issues))
    checks.append(("🔍 质疑者视角", skeptic_issues, 25))
    
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
    
    score += 25 if len(op_issues) == 0 else max(0, 25 - 5 * len(op_issues))
    checks.append(("⚙️ 操盘手视角", op_issues, 25))
    
    # ─── 4. CEO视角（你） ───
    ceo_issues = []
    # Would Pen approve this?
    if "we manufacture" in message.lower():
        ceo_issues.append("装工厂了")
    if "shenzhen" in message.lower() and "China" not in message:
        ceo_issues.append("只写深圳没写中国")
    if "just" in message.lower() and "?" not in message[-20:]:
        ceo_issues.append("语气不够自信")
    
    score += 25 if len(ceo_issues) == 0 else max(0, 25 - 5 * len(ceo_issues))
    checks.append(("👑 CEO视角", ceo_issues, 25))
    
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
    
    return score >= 90, score, checks

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
