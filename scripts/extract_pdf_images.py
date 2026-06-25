#!/usr/bin/env python3
"""Extract JPEG images from scanned PDF pages using raw stream extraction"""
import re, os, zlib

def extract_jpegs_from_pdf(pdf_path, out_dir):
    """Extract JPEG streams from PDF"""
    os.makedirs(out_dir, exist_ok=True)
    
    with open(pdf_path, 'rb') as f:
        data = f.read()
    
    # Find all stream objects between 'stream' and 'endstream'
    streams = []
    pos = 0
    while True:
        s = data.find(b'stream\n', pos)
        if s == -1:
            s = data.find(b'stream ', pos)
        if s == -1:
            break
        
        e = data.find(b'endstream', s)
        if e == -1:
            break
        
        # Extract raw stream data
        start = s + 7  # len('stream\n') or 'stream '
        if data[s+6:s+7] == b' ':
            start = s + 7
        else:
            start = s + 7
            
        raw = data[start:e]
        streams.append(raw)
        pos = e + 9
    
    print(f"Streams found: {len(streams)}")
    
    # Try each stream as JPEG (check for JPEG magic bytes)
    extracted = 0
    for i, raw in enumerate(streams):
        # Try raw - might be JPEG
        if raw[:2] == b'\xff\xd8':
            path = os.path.join(out_dir, f'stream_{i+1}.jpg')
            with open(path, 'wb') as f:
                f.write(raw)
            print(f"  Stream {i+1}: JPEG ({len(raw)/1024:.0f}KB)")
            extracted += 1
            continue
        
        # Try deflate decompressed
        try:
            decompressed = zlib.decompress(raw)
            if decompressed[:2] == b'\xff\xd8':
                path = os.path.join(out_dir, f'stream_{i+1}.jpg')
                with open(path, 'wb') as f:
                    f.write(decompressed)
                print(f"  Stream {i+1}: deflated JPEG ({len(decompressed)/1024:.0f}KB)")
                extracted += 1
                continue
        except:
            pass
        
        # Check if it's already a valid image
        if len(raw) > 1000:
            print(f"  Stream {i+1}: {len(raw)/1024:.0f}KB (not JPEG, skipping)")
    
    return extracted

# Process BLOO POWER catalog
extracted = extract_jpegs_from_pdf(
    'C:/nichenexusglobal/attachments/info/BLOO POWER Catalog2026.pdf',
    'C:/nichenexusglobal/temp_pages/bloo'
)
print(f"\nExtracted: {extracted} images")
