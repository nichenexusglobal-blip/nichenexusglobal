with open('hammer_db.json', 'r', encoding='utf-8') as f:
    text = f.read()

# The error says line 299 column 7
lines = text.split('\n')
print(f"Total lines: {len(lines)}")
print(f"Line 299 content: {lines[298]!r}")
print(f"Line 299 length: {len(lines[298])}")
print(f"Line 299 chars:")
for i, c in enumerate(lines[298]):
    print(f"  {i}: {c!r} (U+{ord(c):04X})")
