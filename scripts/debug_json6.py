with open('hammer_db.json', 'r', encoding='utf-8') as f:
    text = f.read()

# The error says line 299, col 7. Let's look at lines 296-302
lines = text.split('\n')
for i in range(295, min(303, len(lines))):
    line_num = i + 1
    print(f"Line {line_num}: {lines[i][:100]!r}")

# Find the notes string content and verify it's properly closed
# Search for "notes": "PF2000... pattern
import re
# Find the PiForz notes value
idx = text.find('"PiForz"')
if idx >= 0:
    # Find the notes field in PiForz section
    nidx = text.find('"notes"', idx)
    if nidx >= 0:
        # Find the opening " of the value
        val_start = text.find('"', nidx + 7) + 1
        # Find the closing " - needs to handle escaped quotes inside
        in_str = True
        i = val_start
        while i < len(text):
            if text[i] == '\\':
                i += 2  # skip escape sequence
                continue
            if text[i] == '"':
                break
            i += 1
        if i < len(text):
            notes_val = text[val_start:i]
            print(f"\nNotes starts at char {val_start}, ends at char {i}")
            print(f"Notes value ({len(notes_val)} chars): {notes_val[:150]!r}...")
            # Check for raw newlines in the notes value
            for j, c in enumerate(notes_val):
                if c == '\n':
                    print(f"  RAW NEWLINE at char {val_start + j}")
                    break
                if c == '\r':
                    print(f"  RAW CR at char {val_start + j}")
                    break
            else:
                print("  No raw newlines/CRs in notes - good")
        else:
            print(f"Could not find closing quote - last 50 chars: {text[i-50:]!r}")
