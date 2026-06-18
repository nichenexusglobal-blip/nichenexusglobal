import json
with open('hammer_db.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the problematic notes field
idx_start = content.find('"notes": "')
if idx_start >= 0:
    idx_start += len('"notes": "')
    for i in range(idx_start, idx_start + 1000):
        if content[i] == '"' and i+1 < len(content) and content[i+1] == ',':
            # Check backslash
            if content[i-1] != '\\':
                notes_val = content[idx_start:i]
                raw_newlines = [(j, repr(notes_val[j])) for j in range(len(notes_val)) if notes_val[j] == '\n']
                print(f"Notes value length: {len(notes_val)}")
                print(f"Raw newlines in notes: {len(raw_newlines)}")
                for pos, rep in raw_newlines[:5]:
                    ctx_before = repr(notes_val[max(0,pos-10):pos])
                    ctx_after = repr(notes_val[pos:pos+10])
                    print(f"  At pos {pos}: {ctx_before} -> {ctx_after}")
                break
else:
    print("Could not find notes field")
