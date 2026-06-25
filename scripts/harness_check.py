#!/usr/bin/env python3
"""Harness integrity check — computes SHA256 hashes and compares against .harness.json"""
import hashlib, json, sys
from collections import Counter
from pathlib import Path

DIR = Path("C:/nichenexusglobal")
MONITORED = [
    "universal_send_gate.py",
    "precision_gate.py",
    "precision_bullet_gate.py",
    "supplier_rfq_gate.py",
    "hammer_db.json",
]

harness_path = DIR / ".harness.json"
if not harness_path.exists():
    print("FATAL: .harness.json not found at", harness_path)
    sys.exit(1)

with open(harness_path) as f:
    harness = json.load(f)
expected = harness["checksums"]

print("=" * 70)
print("HARNESS INTEGRITY CHECK - 2026-06-21")
print("=" * 70)

all_ok = True
results = {}

for fname in MONITORED:
    path = DIR / fname
    exp = expected.get(fname, "MISSING")
    if not path.exists():
        print(f"  {fname}: FILE NOT FOUND")
        all_ok = False
        results[fname] = "MISSING"
        continue
    cur = hashlib.sha256(path.read_bytes()).hexdigest()
    ok = cur == exp
    status = "OK" if ok else "MISMATCH"
    if not ok:
        all_ok = False
    print(f"  {fname}: {status}  (exp={exp[:16]}... cur={cur[:16]}...)")
    results[fname] = "OK" if ok else "MISMATCH"

# Violation summary
violations = harness.get("violations", [])
v_files = Counter(v["file"] for v in violations)

print()
print("-" * 70)
if all_ok:
    print("OVERALL: ALL INTEGRITY CHECKS PASSED")
else:
    print("OVERALL: INTEGRITY VIOLATIONS DETECTED")
print()

print(f"Violations in .harness.json: {len(violations)} total")
for f, c in v_files.most_common():
    print(f"  {f}: {c} violations")
    latest = [v for v in violations if v["file"] == f]
    if latest:
        l = latest[-1]
        print(f"     latest: {l['time'][:19]}  ({l['old_hash']} -> {l['new_hash']})")

print()
print("Other notes:")
ok_file = len([v for v in harness.get("approved_changes", []) if v["file"] == "harness.py"]) > 0
print(f"  harness.py: MISSING from disk (but referenced in checksums)")
print(f"  Last approved change: {harness['approved_changes'][-1]['time'][:10]} - {harness['approved_changes'][-1]['file']}")
print(f"  Approved changes in history: {len(harness.get('approved_changes', []))}")
if not all_ok:
    print()
    print("RECOMMENDATION: Review and approve/reject pending changes.")
print("=" * 70)
