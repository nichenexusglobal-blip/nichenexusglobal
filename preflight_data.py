#!/usr/bin/env python3
"""PRE-FLIGHT: Run before any data write or send. Blocks if issues found."""
import json, os, subprocess

WORKDIR = "C:/nichenexusglobal"
errors = []
warnings = []

# ─── CHECK 1: Bullets DB valid ───
try:
    with open(f"{WORKDIR}/bullets_db.json") as f:
        bdb = json.load(f)
    wa = bdb.get("whatsapp_bullets", [])
    em = bdb.get("email_bullets", [])
    print(f"✅ bullets_db.json: {len(wa)} WA + {len(em)} email")
except Exception as e:
    errors.append(f"bullets_db.json corrupt: {e}")

# ─── CHECK 2: Hammer DB valid ───
try:
    with open(f"{WORKDIR}/hammer_db.json") as f:
        hdb = json.load(f)
    total = hdb.get("meta", {}).get("total_hammers", "?")
    print(f"✅ hammer_db.json: {total} hammers")
except Exception as e:
    errors.append(f"hammer_db.json corrupt: {e}")

# ─── CHECK 3: Product data valid ───
pd_dir = f"{WORKDIR}/product_data"
if os.path.exists(pd_dir):
    for fname in os.listdir(pd_dir):
        if fname.endswith(".json"):
            try:
                with open(f"{pd_dir}/{fname}") as f:
                    json.load(f)
                print(f"✅ product_data/{fname}")
            except Exception as e:
                errors.append(f"product_data/{fname}: {e}")

# ─── CHECK 4: GitHub sync ───
r = subprocess.run(["git", "status", "--porcelain"], cwd=WORKDIR, capture_output=True, text=True, timeout=10)
if r.stdout.strip():
    # Check if any critical files are uncommitted
    critical = ["hammer_db.json", "bullets_db.json"]
    for line in r.stdout.strip().split("\n"):
        fname = line.strip().split()[-1] if line.strip() else ""
        if fname in critical:
            warnings.append(f"⚠️ {fname} has uncommitted changes!")
    print(f"⚠️ {len(r.stdout.strip().split(chr(10)))} uncommitted files")
else:
    print(f"✅ Git clean")

# ─── CHECK 5: Recent GitHub push ───
r = subprocess.run(["git", "log", "-1", "--format=%cr"], cwd=WORKDIR, capture_output=True, text=True, timeout=5)
last_push = r.stdout.strip()
print(f"✅ Last push: {last_push}")

# ─── RESULTS ───
print(f"\n{'='*40}")
if errors:
    print(f"❌ BLOCKED: {len(errors)} errors")
    for e in errors:
        print(f"  {e}")
    exit(1)
elif warnings:
    print(f"⚠️ PASSED with {len(warnings)} warnings")
    for w in warnings:
        print(f"  {w}")
else:
    print(f"✅ ALL CLEAR - proceed with confidence")
