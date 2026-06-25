"""Convert SOUOP catalog PDF to images for viewing"""
from pdf2image import convert_from_path
import os

pdf_path = "C:/nichenexusglobal/attachments/supplier_docs/E-brochure of portable power stations from Pordie  Energy.pdf"
out_dir = "C:/nichenexusglobal/attachments/supplier_docs/souop_pages"
os.makedirs(out_dir, exist_ok=True)

# Convert to images
images = convert_from_path(pdf_path, dpi=200, first_page=1, last_page=20)
print(f"Converted {len(images)} pages to images")

for i, img in enumerate(images):
    fpath = os.path.join(out_dir, f"page_{i+1:02d}.png")
    img.save(fpath, "PNG")
    size_kb = os.path.getsize(fpath) / 1024
    print(f"  page_{i+1:02d}.png ({size_kb:.0f} KB)")

print(f"\n✅ Saved to: {out_dir}")
