import json

with open('hammer_db.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Find PiForz notes specifically
idx = content.find('"PiForz"')
if idx >= 0:
    section = content[idx:idx+1000]
    print(f"PiForz section starts at byte {idx}")
    print(f"Repr of first 300 chars:")
    print(repr(section[:300]))
    print()
    # Find the notes field in this section
    nidx = section.find('"notes"')
    if nidx >= 0:
        after_notes = section[nidx+len('"notes"'):]
        print(f"After 'notes': {repr(after_notes[:200])}")
else:
    print("PiForz not found by name, searching for piforz.com")
    idx2 = content.find('piforz.com')
    if idx2 >= 0:
        print(f"piforz.com at byte {idx2}")
        print(repr(content[idx2-50:idx2+500]))
