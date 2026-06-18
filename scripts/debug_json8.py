import json

with open('hammer_db.json', 'r', encoding='utf-8') as f:
    text = f.read()

# Find the hammers array of verified_suppliers
# Parse only up to where I know it's good (just before PiForz)
arr_start = text.find('"hammers"')
arr_start = text.find('[', arr_start)

# Try smaller and smaller slices to find the break
# First find the PiForz entry start
piforz_start = text.find('"PiForz"', arr_start)

# Try parsing just before PiForz
test1 = text[arr_start : piforz_start + 200]
try:
    json.loads(test1)
    print(f"Parse OK up to PiForz+200")
except json.JSONDecodeError as e:
    print(f"FAIL at PiForz start: {e}")

# Try much smaller - parse the entry before PiForz
# Find "rank": 1 (first entry)
rank1 = text.find('"rank": 1', arr_start)
if rank1 >= 0:
    # Find the "name": "Shenzhen Taico Technology" (the first entry)
    name1_start = text.find('"name"', rank1)
    name1_val_start = text.find('"', name1_start + 6) + 1
    name1_val_end = text.find('"', name1_val_start)
    name1 = text[name1_val_start:name1_val_end]
    print(f"First entry name: {name1}")

# Let's try parsing entry by entry
# Find all top-level objects in the hammers array
depth = 0
obj_starts = []
in_str = False
escaped = False
for i in range(arr_start, min(arr_start + 10000, len(text))):
    if escaped:
        escaped = False
        continue
    if in_str:
        if text[i] == '\\':
            escaped = True
        elif text[i] == '"':
            in_str = False
        continue
    if text[i] == '"':
        in_str = True
        continue
    if text[i] == '{':
        depth += 1
        if depth == 1:
            obj_starts.append(i)
    elif text[i] == '}':
        depth -= 1

print(f"\nFound {len(obj_starts)} objects in hammers array")
print(f"First few object starts: {obj_starts[:5]}")

# Try to parse first 5 entries
for n in range(min(5, len(obj_starts)-1)):
    start = obj_starts[n]
    end = obj_starts[n+1] if n+1 < len(obj_starts) else min(start + 2000, len(text))
    test = text[start:end]
    try:
        obj = json.loads(test)
        name = obj.get('name', 'unknown')
        print(f"  Entry {n+1}: {name} - OK")
    except json.JSONDecodeError as e:
        print(f"  Entry {n+1}: FAIL - {e}")
        print(f"  Context: {test[e.pos-20:e.pos+20]!r}")
        break
