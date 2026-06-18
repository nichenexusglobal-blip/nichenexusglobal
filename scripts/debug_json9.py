import json

with open('hammer_db.json', 'r', encoding='utf-8') as f:
    text = f.read()

# Find the hammers array of verified_suppliers
arr_start = text.find('"hammers"')
arr_start = text.find('[', arr_start)

# Parse the first object (rank 1 - Shenzhen Taico Technology)
# It starts at char 609 after the [
first_obj = text[arr_start + 609 : arr_start + 1030]
print(f"First object text:")
print(first_obj)
print()
print(f"Repr: {first_obj!r}")
print()

# Find the actual problem - the notes field has "携带电站" which has Chinese chars
# Check if the closing " is proper
try:
    obj = json.loads(first_obj)
    print("Parse OK")
except json.JSONDecodeError as e:
    print(f"Parse failed at pos {e.pos}: {e}")
    print(f"Context: {first_obj[e.pos-20:e.pos+40]}")
