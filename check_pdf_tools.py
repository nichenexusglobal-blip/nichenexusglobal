"""Find available PDF tools and extract text"""
import subprocess, sys

# Check what's available
for cmd in ["pdftotext", "pdftotext.exe"]:
    r = subprocess.run(["where", cmd], capture_output=True, text=True, timeout=5)
    print(f"{cmd}: {'✅' if r.returncode == 0 else '❌'} {r.stdout.strip()[:50]}")

# Check python packages
for mod in ["PyPDF2", "pypdf", "pdfminer", "pdfminer.high_level", "fitz", "pdfplumber", "pdfminer.six"]:
    try:
        __import__(mod.split(".")[0])
        print(f"{mod}: ✅ installed")
    except:
        print(f"{mod}: ❌ not installed")

# Try pip list for pdf-related
r = subprocess.run([sys.executable, "-m", "pip", "list", "--format=columns"], capture_output=True, text=True, timeout=15)
pdf_pkgs = [l for l in r.stdout.split("\n") if "pdf" in l.lower()]
if pdf_pkgs:
    print(f"\nInstalled PDF packages: {pdf_pkgs}")
