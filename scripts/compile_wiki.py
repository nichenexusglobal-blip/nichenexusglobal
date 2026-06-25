#!/usr/bin/env python3
"""
Knowledge Compiler v1 - Karpathy's knowledge compilation model
Reads raw/ directory, compiles into structured wiki/ knowledge base
"""
import os, json, re
from datetime import datetime

BASE = "C:/nichenexusglobal"
RAW = f"{BASE}/raw"
WIKI = f"{BASE}/wiki"

def read_md(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_concepts(text):
    """Extract key concepts from text for cross-linking"""
    concepts = []
    patterns = [
        r'(?i)(?:^|\n)#+\s*(.+?)(?:\n|$)',  # Headers
        r'(?i)\b(LiFePO4|FOB|EXW|OEM|ODM|CE/FCC|MoQ|B2B|B2C|MPPT|UPS|ESS|BMS|LFP|NMC|Wh|kWh)\b',  # Tech terms
        r'(?i)\b(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b',  # Proper names
    ]
    for p in patterns:
        found = re.findall(p, text)
        concepts.extend(found)
    return list(set(concepts))[:20]

def compile_suppliers():
    """Compile supplier data into wiki/products/"""
    suppliers = {}
    for f in os.listdir(f"{RAW}/suppliers"):
        if f.endswith(".md"):
            name = f.replace(".md", "").replace("_", " ").title()
            content = read_md(f"{RAW}/suppliers/{f}")
            concepts = extract_concepts(content)
            suppliers[f] = {
                "name": name,
                "concepts": concepts,
                "source": f"raw/suppliers/{f}",
                "summary": content[:200]
            }
    
    # Write product index
    with open(f"{WIKI}/products/_index.md", "w") as f:
        f.write("# Products Knowledge Base\n\n")
        f.write(f"Compiled: {datetime.now().isoformat()}\n\n")
        f.write("## Suppliers\n\n")
        for _, s in sorted(suppliers.items()):
            f.write(f"- [{s['name']}]({s['source']})\n")
            f.write(f"  - Concepts: {', '.join(s['concepts'][:8])}\n\n")
    
    # Copy supplier files to wiki/products for direct access
    for f in os.listdir(f"{RAW}/suppliers"):
        if f.endswith(".md"):
            content = read_md(f"{RAW}/suppliers/{f}")
            with open(f"{WIKI}/products/{f}", "w") as fh:
                fh.write(content)
    print(f"  📄 wiki/products/ - supplier files copied")

def compile_lessons():
    """Compile lessons into wiki/operations/"""
    lessons = {}
    for f in os.listdir(f"{RAW}/lessons"):
        if f.endswith(".md"):
            content = read_md(f"{RAW}/lessons/{f}")
            concepts = extract_concepts(content)
            lessons[f] = {"concepts": concepts, "source": f"raw/lessons/{f}"}
    
    with open(f"{WIKI}/operations/_index.md", "w") as f:
        f.write("# Operations & Discipline\n\n")
        f.write(f"Compiled: {datetime.now().isoformat()}\n\n")
        for name, l in sorted(lessons.items()):
            f.write(f"- [{name.replace('_',' ').title()}]({l['source']})\n")
    
    print(f"  📚 wiki/operations/_index.md ({len(lessons)} lessons indexed)")

def build_cross_references():
    """Build cross-reference index linking all wiki content"""
    all_concepts = {}
    for root, dirs, files in os.walk(WIKI):
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)
                content = read_md(path)
                concepts = extract_concepts(content)
                for c in concepts:
                    if c not in all_concepts:
                        all_concepts[c] = []
                    all_concepts[c].append(os.path.relpath(path, WIKI))
    
    with open(f"{WIKI}/_cross_ref.md", "w") as f:
        f.write("# Cross-Reference Index\n\n")
        for concept, refs in sorted(all_concepts.items()):
            if len(refs) > 1:  # Only show cross-linked concepts
                f.write(f"- **{concept}** appears in: {', '.join(refs)}\n")
    
    print(f"  🔗 wiki/_cross_ref.md ({sum(1 for v in all_concepts.values() if len(v)>1)} cross-linked concepts)")

# Run compilation
print("Knowledge Compiler v1")
print("=" * 40)
compile_suppliers()
compile_lessons()
build_cross_references()

# Update manifest
with open(f"{WIKI}/_manifest.json") as f:
    manifest = json.load(f)
manifest["last_compiled"] = datetime.now().isoformat()
manifest["file_count"] = sum(len(files) for _, _, files in os.walk(WIKI))
with open(f"{WIKI}/_manifest.json", "w") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"\n✅ Compilation complete")
print(f"   Wiki: {manifest['file_count']} files")
print(f"   Raw: {sum(len(files) for _,_,files in os.walk(RAW))} sources")
