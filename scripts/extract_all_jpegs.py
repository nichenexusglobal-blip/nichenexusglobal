#!/usr/bin/env python3
"""Generic JPEG extraction from PDF streams"""
import os

def extract_all_jpegs(pdf_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    
    with open(pdf_path, 'rb') as f:
        data = f.read()
    
    # Find ALL occurrences of JPEG start marker within the file
    # JPEG starts with FF D8 FF
    count = 0
    pos = 0
    while True:
        start = data.find(b'\xff\xd8\xff', pos)
        if start == -1:
            break
        
        # Find JPEG end marker FF D9
        end = data.find(b'\xff\xd9', start)
        if end == -1:
            break
        
        jpeg_data = data[start:end+2]
        
        # Save to file
        path = os.path.join(out_dir, f'page_{count+1}.jpg')
        with open(path, 'wb') as f:
            f.write(jpeg_data)
        
        print(f"  Page {count+1}: {len(jpeg_data)/1024:.0f}KB at offset {start}")
        count += 1
        pos = end + 2
    
    return count

pdfs = [
    ('BLOO POWER', 'C:/nichenexusglobal/attachments/info/BLOO POWER Catalog2026.pdf'),
    ('Lansine', 'C:/nichenexusglobal/attachments/admin/LanX CatalogNew压缩.pdf'),
    ('TOYAR', 'C:/nichenexusglobal/attachments/anson.le2002/PPS Catalog TOYAR  2026.pdf'),
]

for name, path in pdfs:
    print(f"\n=== {name} ===")
    out = f'C:/nichenexusglobal/temp_pages/{name.lower().replace(" ","_")}'
    c = extract_all_jpegs(path, out)
    print(f"Total: {c} pages")
