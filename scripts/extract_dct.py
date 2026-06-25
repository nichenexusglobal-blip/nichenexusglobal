#!/usr/bin/env python3
"""Extract DCTDecode JPEG streams from PDF properly"""
import re, os, zlib

def extract_dct_jpegs(pdf_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    
    with open(pdf_path, 'rb') as f:
        data = f.read()
    
    # Find DCTDecode filters and their streams
    # Pattern: /Filter /DCTDecode ... stream\n...data...\nendstream
    pattern = rb'/Filter\s*/DCTDecode.*?stream\n(.+?)\nendstream'
    matches = list(re.finditer(pattern, data, re.DOTALL))
    
    print(f"DCTDecode streams found: {len(matches)}")
    
    count = 0
    for i, m in enumerate(matches):
        raw = m.group(1)
        # Try to find JPEG start/end markers
        jpeg_start = raw.find(b'\xff\xd8\xff')
        if jpeg_start >= 0:
            jpeg_data = raw[jpeg_start:]
            # Find JPEG end
            jpeg_end = jpeg_data.find(b'\xff\xd9')
            if jpeg_end >= 0:
                jpeg_data = jpeg_data[:jpeg_end+2]
            
            path = os.path.join(out_dir, f'dct_page_{count+1}.jpg')
            with open(path, 'wb') as f:
                f.write(jpeg_data)
            print(f"  Page {count+1}: {len(jpeg_data)/1024:.0f}KB")
            count += 1
    
    return count

print("=== BLOO POWER Catalog ===")
c = extract_dct_jpegs(
    'C:/nichenexusglobal/attachments/info/BLOO POWER Catalog2026.pdf',
    'C:/nichenexusglobal/temp_pages/bloo'
)
print(f"Total pages extracted: {c}")
