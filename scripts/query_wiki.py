#!/usr/bin/env python3
"""Query the knowledge wiki"""
import os, glob, json, re

BASE = "C:/nichenexusglobal"
WIKI = f"{BASE}/wiki"

def search(term):
    results = []
    for root, dirs, files in os.walk(WIKI):
        for f in files:
            if f.endswith(".md") and not f.startswith("_"):
                path = os.path.join(root, f)
                with open(path) as fh:
                    content = fh.read()
                if term.lower() in content.lower():
                    lines = content.split("\n")
                    matches = [(i, l.strip()) for i, l in enumerate(lines) if term.lower() in l.lower()]
                    results.append({
                        "file": os.path.relpath(path, WIKI),
                        "matches": matches[:3],
                        "preview": content[:200]
                    })
    return results

def show_wiki():
    print("=" * 50)
    print("NNG KNOWLEDGE WIKI")
    print("=" * 50)
    print(f"\nRaw sources ({len(os.listdir(f'{BASE}/raw/suppliers'))} suppliers + lessons):")
    for f in sorted(os.listdir(f"{BASE}/raw/suppliers")):
        sz = os.path.getsize(f"{BASE}/raw/suppliers/{f}") // 1024
        print(f"  📄 {f} ({sz}KB)")
    
    print(f"\nWiki ({len([f for f in os.listdir(WIKI) if f.endswith('.md')])} index files):")
    for f in sorted(os.listdir(WIKI)):
        if f.endswith(".md"):
            print(f"  📚 {f}")

show_wiki()
