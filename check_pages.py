"""Check page image files"""
import os
d = "C:/nichenexusglobal/attachments/supplier_docs/souop_pages"
files = sorted(os.listdir(d))
for f in files:
    size = os.path.getsize(os.path.join(d, f)) / 1024
    print(f"{f}: {size:.0f} KB")
