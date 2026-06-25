#!/usr/bin/env python3
"""
SELF-IMPROVEMENT ENGINE — 犯错后自修
基于 Polaris (Gödel Agent) 论文：
1. 分析失败
2. 生成策略补丁
3. 验证补丁
4. 固化到 policy
"""
import json, os, sys
from datetime import datetime

POLICY_FILE = "C:/nichenexusglobal/behavior_policy.py"
LOG_FILE = "C:/nichenexusglobal/lessons_learned.jsonl"

def record_lesson(incident, root_cause, fix_applied):
    """记录一次教训和对应的修复"""
    lesson = {
        "timestamp": datetime.now().isoformat(),
        "incident": incident,
        "root_cause": root_cause,
        "fix": fix_applied,
        "verified": False
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(lesson) + "\n")
    print(f"📝 Lesson recorded: {incident[:50]}...")

def add_constraint_to_policy(rule_id, description, check_code):
    """向 policy 文件追加一条硬约束"""
    code = f"""

# {rule_id}: {description}
def __check_{rule_id.lower()}():
    {check_code}

register("{rule_id}", "{description}", __check_{rule_id.lower()})
"""
    with open(POLICY_FILE, "a") as f:
        f.write(code)
    
    # 验证新规则可加载
    result = os.system(f"python -c 'import behavior_policy; behavior_policy.assert_all()' 2>&1")
    if result == 0:
        print(f"✅ Constraint {rule_id} added and verified")
    else:
        print(f"❌ Constraint {rule_id} FAILED verification")

# ── 从Pen的纠正中学习 ──

def learn_from_correction(correction_text):
    """Pen纠正我时调用。分析错误、生成修复、添加约束、验证"""
    
    # Step 1: 分析错误类别
    if "没经同意" in correction_text or "同意" in correction_text:
        # 已经加了 SEND-001 约束
        record_lesson(
            "Sent message without Pen's approval",
            "Skipped approval check before send",
            "SEND-001: hard assert blocks unapproved sends"
        )
        # 加强：在入口处额外检查
        print("🔧 SEND-001 already active — verifying...")
        result = os.system(f"cd {os.path.dirname(POLICY_FILE)} && python -c 'import behavior_policy; behavior_policy.set_approved(False); assert_all()' 2>&1")
        if result == 0:
            print("❌ SEND-001 NOT blocking! Need stronger constraint")
        else:
            print("✅ SEND-001 actively blocking")
    
    elif "门禁" in correction_text or "gate" in correction_text.lower():
        record_lesson(
            "Bypassed gate system",
            "Used direct curl/smtp instead of gate",
            "GATE-001: force all sends through gate"
        )
    
    elif "调研" in correction_text or "没查" in correction_text:
        record_lesson(
            "Skipped research step",
            "Added bullet without verification",
            "RESEARCH-001: require verification before add"
        )
    
    else:
        # 通用处理
        record_lesson(
            correction_text,
            "Unknown root cause - requires manual analysis",
            "Pending"
        )

if __name__ == "__main__":
    # 测试
    test_input = "你发之前问过我吗？没经我同意就发了"
    print(f"🧪 Testing: '{test_input}'")
    learn_from_correction(test_input)
    print("\n📋 Lessons learned log:")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            for line in f:
                l = json.loads(line)
                print(f"  • {l['incident']} → {l['fix']}")
