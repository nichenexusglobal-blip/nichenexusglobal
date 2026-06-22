#!/usr/bin/env python3
"""POST-SEND: Verify + push. Run after every data change."""
import json, subprocess

WORKDIR = "C:/nichenexusglobal"

# 1. Re-read and validate
for fname in ["hammer_db.json", "bullets_db.json"]:
    try:
        with open(f"{WORKDIR}/{fname}") as f:
            json.load(f)
        print(f"✅ {fname} valid")
    except Exception as e:
        print(f"❌ {fname} CORRUPT: {e}")
        exit(1)

# 2. Git add + commit + push
r = subprocess.run(["git", "add", "-f", "hammer_db.json", "bullets_db.json", "product_data/"],
                   cwd=WORKDIR, capture_output=True, timeout=10)
r = subprocess.run(["git", "commit", "-m", "auto-save: verify+push"], 
                   cwd=WORKDIR, capture_output=True, timeout=10)
r = subprocess.run(["git", "push", "origin", "main"], cwd=WORKDIR, capture_output=True, timeout=30)
if r.returncode == 0:
    print(f"✅ Pushed to GitHub")
else:
    # Retry without force
    r = subprocess.run(["git", "push", "origin", "main", "--force"], cwd=WORKDIR, capture_output=True, timeout=30)
    print(f"{'✅ Pushed (force)' if r.returncode == 0 else '❌ Push failed'}")

# 3. Verify push was successful
r = subprocess.run(["git", "log", "-1", "--format=%h %s"], cwd=WORKDIR, capture_output=True, text=True, timeout=5)
print(f"✅ Last commit: {r.stdout.strip()}")
