#!/usr/bin/env python3
"""
Harness — 缰绳系统v1
硬约束：代码修改审计 + 调研证据链 + 违规自动上报
"""
import json, os, hashlib, sys, subprocess
from datetime import datetime

WORKDIR = r"D:\nichenexusglobal"
if not os.path.exists(WORKDIR):
    # Fallback to C: if D: doesn't exist
    fallback = r"C:\nichenexusglobal"
    if os.path.exists(fallback):
        WORKDIR = fallback
HARNESS_FILE = os.path.join(WORKDIR, ".harness.json")

# ─── 受保护文件（修改必须走批准） ────────────────────
PROTECTED_FILES = [
    "universal_send_gate.py",
    "precision_gate.py",
    "precision_bullet_gate.py",
    "supplier_rfq_gate.py",
    "hammer_db.json",
]

def get_file_hash(path):
    full = os.path.join(WORKDIR, path)
    if not os.path.exists(full):
        return None
    with open(full, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def load_harness():
    if os.path.exists(HARNESS_FILE):
        with open(HARNESS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"checksums": {}, "approved_changes": [], "violations": []}

def save_harness(data):
    with open(HARNESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def init_checksums():
    """初始化所有受保护文件的checksum"""
    h = load_harness()
    for f in PROTECTED_FILES:
        ch = get_file_hash(f)
        if ch:
            h["checksums"][f] = ch
    save_harness(h)
    print("✅ 缰绳初始化完成 — 受保护文件:", len(PROTECTED_FILES))

def check_integrity():
    """
    检查受保护文件是否有未批准的修改。
    返回: [(file, old_hash, new_hash, status), ...]
    """
    h = load_harness()
    results = []
    for f in PROTECTED_FILES:
        old = h["checksums"].get(f)
        current = get_file_hash(f)
        if old is None:
            results.append((f, "未记录", current[:16] if current else "N/A", "NEW"))
            h["checksums"][f] = current
        elif current and current != old:
            # 查这个修改有没有记录在approved_changes里
            approved = False
            for change in h["approved_changes"]:
                if change["file"] == f and change["new_hash"] == current:
                    approved = True
                    break
            if not approved:
                results.append((f, old[:16], current[:16], "⚠️ 未批准修改"))
                h["violations"].append({
                    "file": f,
                    "time": datetime.now().isoformat(),
                    "old_hash": old[:16],
                    "new_hash": current[:16],
                    "status": "unapproved_change"
                })
            else:
                results.append((f, old[:16], current[:16], "✅ 已批准"))
                h["checksums"][f] = current
        elif current:
            results.append((f, old[:16], current[:16], "✅ 一致"))
    save_harness(h)
    return results

def approve_change(file_path, reason=""):
    """批准对某个文件的修改"""
    h = load_harness()
    ch = get_file_hash(file_path)
    if ch:
        h["approved_changes"].append({
            "file": file_path,
            "new_hash": ch,
            "time": datetime.now().isoformat(),
            "reason": reason
        })
        h["checksums"][file_path] = ch
        save_harness(h)
        # 清除此文件的违规记录
        h["violations"] = [v for v in h["violations"] if v["file"] != file_path]
        save_harness(h)
        print(f"✅ 已批准: {file_path} — {reason}")
        return True
    return False

def report_violations():
    """输出所有未解决的违规"""
    h = load_harness()
    if not h["violations"]:
        print("✅ 零违规")
        return
    print(f"⚠️ {len(h['violations'])} 个违规:")
    for v in h["violations"]:
        print(f"  [{v['time']}] {v['file']}: {v['old_hash']} → {v['new_hash']} ({v['status']})")

# ─── 研究证据链 ──────────────────────────────────

def save_research(target_name, target_url, findings, retail_prices=None):
    """保存对某个目标的研究证据"""
    evidence_file = os.path.join(WORKDIR, ".research_evidence.json")
    evidence = []
    if os.path.exists(evidence_file):
        with open(evidence_file, encoding="utf-8") as f:
            evidence = json.load(f)
    
    entry = {
        "target": target_name,
        "url": target_url,
        "time": datetime.now().isoformat(),
        "findings": findings,
        "retail_prices": retail_prices or [],
    }
    evidence.append(entry)
    with open(evidence_file, "w", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2, ensure_ascii=False)
    print(f"📋 研究证据已保存: {target_name}")
    return entry

def get_research(target_name):
    """获取对某个目标的研究证据"""
    evidence_file = os.path.join(WORKDIR, ".research_evidence.json")
    if not os.path.exists(evidence_file):
        return None
    with open(evidence_file, encoding="utf-8") as f:
        evidence = json.load(f)
    for e in reversed(evidence):
        if e["target"].lower() == target_name.lower():
            return e
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python harness.py init|check|approve <file> <reason>|report")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "init":
        init_checksums()
    elif cmd == "check":
        results = check_integrity()
        for f, old, new, status in results:
            print(f"  {status} | {f}")
        if any("未批准" in r[3] for r in results):
            print("\n⚠️ 有未批准的修改！用下面命令批准:")
            print("  python harness.py approve <文件名> \"修改原因\"")
    elif cmd == "approve":
        if len(sys.argv) < 4:
            print("用法: python harness.py approve <文件名> \"修改原因\"")
            sys.exit(1)
        approve_change(sys.argv[2], sys.argv[3])
    elif cmd == "report":
        report_violations()
    else:
        print(f"未知命令: {cmd}")
