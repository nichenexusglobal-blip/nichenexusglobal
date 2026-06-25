#!/usr/bin/env python3
"""Extract images from scanned PDF and dump raw image data info"""
import json, os, re, zlib, struct

def scan_pdf_for_images(pdf_path):
    """Scan PDF for embedded images and dump their info"""
    with open(pdf_path, 'rb') as f:
        data = f.read()
    
    results = {
        'file': os.path.basename(pdf_path),
        'size_kb': len(data) / 1024,
        'pages': 0,
        'images_found': 0,
        'image_sizes': [],
        'text_fragments': [],
    }
    
    # Try to find /Type /Page entries
    pages = re.findall(rb'/Type\s*/Page[^r]', data)
    results['pages'] = len(pages)
    
    # Try to find embedded JPEG/PNG images
    # JPEG markers
    jpegs = re.findall(rb'\xff\xd8\xff[\xe0-\xef][\x00-\xff]{2}[^\x00]*?\xff\xd9', data)
    results['images_found'] += len(jpegs)
    for j in jpegs:
        results['image_sizes'].append(len(j))
    
    # PNG markers
    pngs = re.findall(rb'\x89PNG\r\n\x1a\n[\s\S]*?IEND\xae\x42\x60\x82', data)
    results['images_found'] += len(pngs)
    for p in pngs:
        results['image_sizes'].append(len(p))
    
    # Try to extract any text-like content
    # Look for PDF strings between parentheses
    strings = re.findall(rb'\(([^)]{4,80})\)', data)
    for s in strings:
        try:
            decoded = s.decode('latin-1')
            # Filter out garbage
            if any(c.isalpha() for c in decoded) and sum(c.isalpha() for c in decoded) > len(decoded) * 0.4:
                results['text_fragments'].append(decoded)
        except:
            pass
    
    return results

# Process each scanned PDF
pdfs = [
    'C:/nichenexusglobal/attachments/info/BLOO POWER Catalog2026.pdf',
    'C:/nichenexusglobal/attachments/admin/LanX CatalogNew压缩.pdf',
    'C:/nichenexusglobal/attachments/anson.le2002/PPS Catalog TOYAR  2026.pdf',
]

for pdf_path in pdfs:
    if not os.path.exists(pdf_path):
        print(f"\n=== {os.path.basename(pdf_path)} — NOT FOUND ===")
        continue
    
    r = scan_pdf_for_images(pdf_path)
    print(f"\n=== {os.path.basename(pdf_path)} ===")
    print(f"  Size: {r['size_kb']:.0f}KB")
    print(f"  Pages: {r['pages']}")
    print(f"  Embedded images: {r['images_found']} ({len(r['image_sizes'])} found)")
    if r['image_sizes']:
        for i, sz in enumerate(r['image_sizes'][:5]):
            print(f"    Image {i+1}: {sz/1024:.0f}KB")
    if r['text_fragments']:
        print(f"  Text fragments found: {len(r['text_fragments'])}")
        for t in r['text_fragments'][:10]:
            print(f"    - {t[:100]}")
    else:
        print(f"  Text fragments: none — fully scanned/image PDF")
