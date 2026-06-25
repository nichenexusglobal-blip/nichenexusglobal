"""Parse SOUOP/Pordie product catalog PDF"""
import subprocess, json

pdf_path = "C:/nichenexusglobal/attachments/supplier_docs/E-brochure of portable power stations from Pordie  Energy.pdf"

# Try pdftotext
result = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True, timeout=30)
text = result.stdout

if not text.strip():
    # Try pypdf2
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        text = "\n".join([p.extract_text() or "" for p in reader.pages])
    except:
        pass

if not text.strip():
    # Try pdfminer
    try:
        from pdfminer.high_level import extract_text
        text = extract_text(pdf_path)
    except:
        pass

if text.strip():
    lines = text.split("\n")
    print(f"=== PDF 内容 ({len(lines)} lines, {len(text)} chars) ===")
    print()
    
    # Look for product names, models, specs
    keywords = ["model", "power", "wh", "watt", "price", "fob", "$", "voltage", "capacity", "lifepo4", "souop", "pordie"]
    
    # Print first 200 lines
    for i, line in enumerate(lines[:200]):
        print(line)
    
    print(f"\n... ({len(lines)} lines total)")
    
    # Search for key sections
    print("\n=== KEY PRODUCT SECTIONS ===")
    print("=" * 60)
    for i, line in enumerate(lines):
        lower = line.lower()
        if any(k in lower for k in ["model", "specification", "parameter", "product list", "series"]):
            # Print this line + next 5
            print(f"\n[{i}] {line}")
            for j in range(1, 6):
                if i+j < len(lines):
                    print(f"     {lines[i+j]}")
else:
    print("❌ Could not extract text from PDF")
    print(f"File size: {__import__('os').path.getsize(pdf_path) / 1024:.0f} KB")
