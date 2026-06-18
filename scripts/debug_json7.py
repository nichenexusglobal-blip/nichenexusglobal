with open('hammer_db.json', 'r', encoding='utf-8') as f:
    text = f.read()

# Look at chars around 8510-8530
for i in range(8505, min(8535, len(text))):
    c = text[i]
    print(f"  {i}: {c!r} (U+{ord(c):04X})")

# Try to parse just the verified_suppliers section
import json
# Find the verified_suppliers array
vs_start = text.find('"verified_suppliers"')
if vs_start >= 0:
    # Find the hammers array
    h_start = text.find('"hammers"', vs_start)
    if h_start >= 0:
        # Find the opening [
        arr_start = text.find('[', h_start)
        if arr_start >= 0:
            # Try to parse from this point to a few KB later
            test = text[arr_start:arr_start + 5000]
            # Check if the text up to the problem area is valid
            try:
                json.loads(test)
                print(f"\nTest parse OK for first 5000 chars")
            except json.JSONDecodeError as e:
                print(f"\nTest parse failed at pos {e.pos}: {e}")
                # Show context
                start = max(0, arr_start + e.pos - 30)
                end = min(len(text), arr_start + e.pos + 30)
                print(f"Context: {text[start:end]!r}")
