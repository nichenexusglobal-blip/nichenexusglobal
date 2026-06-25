"""Extract content from SOUOP catalog using PyMuPDF"""
import fitz, os

pdf_path = "C:/nichenexusglobal/attachments/supplier_docs/E-brochure of portable power stations from Pordie  Energy.pdf"
out_dir = "C:/nichenexusglobal/attachments/supplier_docs/souop_pages"
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print(f"📄 PDF: {doc.page_count} pages")

# Text extraction
for page_num in range(doc.page_count):
    page = doc[page_num]
    text = page.get_text()
    if text.strip():
        print(f"\n--- Page {page_num+1} (text) ---")
        print(text[:800])
    
    # Also render as image
    pix = page.get_pixmap(dpi=150)
    img_path = os.path.join(out_dir, f"page_{page_num+1:02d}.png")
    pix.save(img_path)
    print(f"  🖼 Saved: page_{page_num+1:02d}.png ({pix.width}x{pix.height})")

doc.close()
print(f"\n✅ Done. {doc.page_count} pages processed to: {out_dir}")
