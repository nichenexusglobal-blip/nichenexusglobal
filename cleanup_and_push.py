#!/usr/bin/env python3
"""Cleanup temp scripts and git push"""
import os, subprocess

WORKDIR = "C:/nichenexusglobal"

# Remove temp scripts
temp = ["extract_pdfs.py", "extract_pdfs2.py", "parse_pdfs.py", "view_extracts.py", 
        "scan_materials.py", "index_images.py", "link_images.py", "organize_images.py",
        "update_hammer.py", "cleanup.py"]
removed = 0
for f in temp:
    path = os.path.join(WORKDIR, f)
    if os.path.exists(path):
        os.remove(path)
        removed += 1
print(f"Cleaned {removed} temp files")

# Git push (no --force)
r = subprocess.run(["git", "add", "-f", "hammer_db.json", "product_images/"],
    cwd=WORKDIR, capture_output=True, text=True)
print(f"git add: {r.stdout}{r.stderr[:100]}")

r = subprocess.run(["git", "commit", "-m", "added product images to hammer DB"],
    cwd=WORKDIR, capture_output=True, text=True)
print(f"git commit: {r.stdout[:200]}{r.stderr[:100]}")

r = subprocess.run(["git", "push", "origin", "main"],
    cwd=WORKDIR, capture_output=True, text=True, timeout=30)
print(f"git push: {r.stdout[:200]}{r.stderr[:100]}")
