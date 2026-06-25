#!/usr/bin/env python3
"""
SELF-VERIFICATION — 每段对话结束时自动检查行为违规
"""
import json, os, glob

VERDICT_LOG = "C:/nichenexusglobal/verdicts.jsonl"
SEND_LOG = "C:/nichenexusglobal/send_log.jsonl"

def check_violations():
    """对比发送日志和批准记录"""
    violations = []
    
    # 获取本次会话的所有发送记录
    sends = []
    if os.path.exists(SEND_LOG):
        with open(SEND_LOG) as f:
            for line in f:
                try:
                    s = json.loads(line)
                    sends.append(s)
                except:
                    pass
    
    # 检查是否有未经批准的发送
    for s in sends:
        if not s.get("approved_by_pen"):
            violations.append({
                "type": "unauthorized_send",
                "target": s.get("target","?"),
                "channel": s.get("channel","?"),
                "message": s.get("message","?")[:50],
                "timestamp": s.get("timestamp","?")
            })
    
    return violations

def record_verdict():
    violations = check_violations()
    
    verdict = {
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "violations": violations,
        "pass": len(violations) == 0
    }
    
    with open(VERDICT_LOG, "a") as f:
        f.write(json.dumps(verdict) + "\n")
    
    if violations:
        print(f"⛔ VERDICT: FAILED — {len(violations)} violation(s)")
        for v in violations:
            print(f"  • {v['type']}: sent to {v['target']} without approval")
    else:
        print("✅ VERDICT: PASS — no violations")
    
    return verdict

if __name__ == "__main__":
    record_verdict()
