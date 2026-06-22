#!/usr/bin/env python3
"""
BEHAVIOR POLICY v1 — Hard constraints, not memory notes.

每次Pen纠正我，我在这里加一条硬性规则和一对应测试。
规则要：非人类可撤销、代码级中断、可验证。
"""
import os, sys, json
from datetime import datetime

# ── Registry of hard constraints ──────────────────────
# 每条规则：{id, rule, created, enforcement, test}
CONSTRAINTS = []

def register(rule_id, description, check_fn):
    """注册硬性规则。check_fn返回True=通过，False=违规"""
    CONSTRAINTS.append({
        "id": rule_id,
        "description": description,
        "created": datetime.now().isoformat(),
        "check": check_fn,
        "enforcement": "hard_assert"
    })

def assert_all():
    """在关键操作前调用——所有规则必须通过"""
    failures = []
    for c in CONSTRAINTS:
        try:
            result = c["check"]()
            if not result:
                failures.append(c["id"])
        except Exception as e:
            failures.append(f"{c['id']}: {e}")
    
    if failures:
        msg = f"⛔ BEHAVIOR BLOCKED — Violated: {', '.join(failures)}"
        print(msg)
        sys.exit(1)
    return True

# ═══════════════════════════════════════════════════════
# RULES START HERE

# Rule 1: 发送前必须有Pen的明确同意
# 所有对外发送操作必须先调用assert_all()
# 如果pen_approved为False，发送被阻断

pen_approved = False  # 每次会话开始时重置

def set_approved(by_user=True):
    global pen_approved
    pen_approved = by_user

def check_pen_approval():
    return pen_approved is True

register("SEND-001", "Cannot send any message without Pen's explicit '发'", check_pen_approval)

# Rule 2: Pre-flight check — 操作前自检
import traceback

def pre_flight_check(action_type, context=""):
    """任何关键操作前调用。检查环境、授权、数据完整性"""
    checks_passed = True
    warnings = []
    
    if action_type == "send":
        if not pen_approved:
            warnings.append("⛔ SEND BLOCKED: Pen hasn't said '发'")
            checks_passed = False
    
    elif action_type == "add_bullet":
        # 检查是否有完整调研
        if "draft" not in context and "email" not in context:
            warnings.append("⚠ ADD BULLET: No draft or email — are you sure it's researched?")
            checks_passed = False
    
    elif action_type == "modify_system":
        # 检查是否在能修改系统文件
        caller = traceback.extract_stack()[-3].filename
        if "scripts/" not in caller and "behavior_policy" not in caller:
            warnings.append(f"⚠ SYSTEM MOD by unexpected caller: {caller}")
    
    if not checks_passed:
        for w in warnings:
            print(w)
        return False
    return True

register("PREFLIGHT-001", "Pre-flight check before any send operation", lambda: pre_flight_check("send"))

# Rule 2: 已有草稿的子弹才能入库
def check_draft_required():
    # 当调用save_bullet()时必须带draft
    return True  # 暂无条件，后面扩展

register("DRAFT-001", "Bullets must have a draft before saving", check_draft_required)

# Rule 3: Signal Registry — 每次纠正分析遗漏信号
SIGNAL_LOG = "C:/nichenexusglobal/signal_log.jsonl"

def record_missed_signal(incident, missed_signal, proposed_fix):
    """当Pen纠正我时，分析：什么信号在出错前就该被我捕捉到"""
    entry = {
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "incident": incident,
        "missed_signal": missed_signal,
        "proposed_fix": proposed_fix,
        "applied": False
    }
    with open(SIGNAL_LOG, "a") as f:
        f.write(__import__("json").dumps(entry) + "\n")
    print(f"🔍 Signal recorded: missed '{missed_signal}'")

def check_signals():
    """验证是否有未处理的信号。如果有人纠正后还没修，阻断操作"""
    if not os.path.exists(SIGNAL_LOG):
        return True
    with open(SIGNAL_LOG) as f:
        for line in f:
            try:
                entry = __import__("json").loads(line)
                if not entry.get("applied"):
                    print(f"⛔ Unresolved signal: {entry.get('missed_signal','?')}")
                    return False
            except:
                pass
    return True

register("SIGNAL-001", "All detected missed signals must be resolved", check_signals)

# ═══════════════════════════════════════════════════════
# LEVEL 3: 预见错误 → 在Pen发现前自修

FAILURE_PATTERNS = {
    "send_without_approval": {
        "description": "Sent message without asking Pen first",
        "signals": ["curl.*send", "smtp.*send_message", "bridge.*send", "send.*message", "发.*给", "直接发"],
        "reminder": "Pen says '发' before I send. No exceptions."
    },
    "add_unverified_bullet": {
        "description": "Added bullet without proper research",
        "signals": ["web_search.*without.*browser", "add_bullet.*no_draft"],
        "reminder": "Every bullet needs: website check + WhatsApp verification + draft."
    },
    "bypass_gate": {
        "description": "Used raw send instead of gate",
        "signals": ["curl.*POST.*send", "terminal.*send_message"],
        "reminder": "Only send through gate or Pen's explicit terminal command."
    },
    "assume_not_ask": {
        "description": "Made assumptions instead of asking Pen",
        "signals": ["客户.*想要", "应该.*发", "我觉得", "肯定.*想要"],
        "reminder": "When in doubt → ask. Don't guess what Pen wants."
    }
}

# Auto-block categories
AUTO_BLOCK = ["send_without_approval", "bypass_gate", "assume_not_ask"]

def self_review(action_intent, context=""):
    """
    Level 3: 在行动前自我审视。
    检查当前意图是否匹配任何已知的失败模式。
    如果匹配且有风险，主动暂停提醒。
    """
    import re
    
    combined = f"{action_intent} {context}".lower()
    
    for pattern_id, pattern in FAILURE_PATTERNS.items():
        for signal in pattern["signals"]:
            if re.search(signal, combined):
                print(f"\n🔔 L3 WARNING: Pattern '{pattern_id}' detected!")
                print(f"   {pattern['reminder']}")
                
                # If this is a send pattern, block automatically
                if "send" in pattern_id:
                    print("   ⛔ AUTO-BLOCKED — prevent recurring mistake")
                    return False
    
    return True

# Register Level 3 check as a constraint
def l3_self_review_pass():
    # Always passes by default — triggered explicitly by self_review()
    return True

register("L3-001", "Level 3: Self-review before actions", l3_self_review_pass)

# ═══════════════════════════════════════════════════════
# SEND GATE — 唯一出口

def universal_send(chat_id, message, channel="whatsapp"):
    """唯一的发送入口。所有发消息必须走这个函数。"""
    assert_all()  # 所有规则先过一遍
    print(f"✅ Sending to {chat_id} via {channel}")
    # ... 实际发送逻辑

# ── SELF-TEST ──────────────────────────────────────────
if __name__ == "__main__":
    print("🧪 Running self-test...")
    
    # Test: unapproved send should fail
    pen_approved = False
    try:
        assert_all()
        print("❌ FAIL: Should have blocked without approval")
    except SystemExit:
        print("✅ PASS: Blocked unapproved send")
    
    # Test: approved send should pass
    pen_approved = True
    try:
        assert_all()
        print("✅ PASS: Approved send allowed")
    except SystemExit:
        print("❌ FAIL: Should allow approved send")
    
    print(f"\n📋 {len(CONSTRAINTS)} hard constraints active")
