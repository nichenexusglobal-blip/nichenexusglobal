with open('hammer_db.json', 'rb') as f:
    content = f.read()

BS = chr(92)
print(f"Total file size: {len(content)} bytes")
print(f"Char 8510-8530:")
for i in range(8510, min(8530, len(content))):
    print(f"  {i}: {chr(content[i])!r} (0x{content[i]:02x})")

lines = content.split(b'\n')
print(f"\nTotal lines: {len(lines)}")
if len(lines) > 298:
    line298 = lines[297]
    line299 = lines[298]
    line300 = lines[299]
    print(f"Line 298 (0-indexed 297, len={len(line298)}): {line298[:80]}")
    print(f"Line 298 ending: {line298[-30:]}")
    print(f"Line 299 (0-indexed 298, len={len(line299)}): {line299[:80]}")
    print(f"Line 300 (0-indexed 299, len={len(line300)}): {line300[:80]}")

print(f"\nFirst 4 bytes: {content[:4].hex()}")
bom = b'\xef\xbb\xbf'
print(f"Has BOM: {content[:3] == bom}")

# Check for any non-ASCII/non-UTF8
bad = [(i, content[i]) for i in range(len(content)) if content[i] > 127]
print(f"Non-ASCII bytes: {len(bad)}")
if bad:
    for i, b in bad[:10]:
        ctx = content[max(0,i-5):i+5]
        print(f"  pos {i}: 0x{b:02x} ctx: {ctx}")
