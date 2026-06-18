# Check the raw bytes of the file around the PiForz notes
with open('hammer_db.json', 'rb') as f:
    content = f.read()

# Find PiForz section
idx = content.find(b'PiForz')
if idx >= 0:
    # Find the notes field
    nidx = content.find(b'"notes"', idx)
    if nidx >= 0:
        # Show raw bytes from the start of notes value to some chars after
        start = nidx
        end = min(nidx + 500, len(content))
        chunk = content[start:end]
        print(f"Raw bytes from 'notes' ({start} to {end}):")
        # Print as hex + ascii
        for i in range(0, len(chunk), 32):
            hex_part = ' '.join(f'{b:02x}' for b in chunk[i:i+16])
            ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk[i:i+16])
            print(f"  {start+i:6d}: {hex_part:48s} {ascii_part}")
        print()
        print(f"Total file size: {len(content)} bytes")
        
        # Now check for the exact closing "
        val_start = nidx + len(b'"notes"')
        # Skip the : " part
        val_start = content.find(b'"', val_start) + 1
        # Find the closing "
        for i in range(val_start, val_start + 300):
            if content[i] == ord('"'):
                prev_byte = content[i-1]
                # Check if this is an escaped quote or the closing quote
                # In JSON, closing " would be preceded by non-backslash
                if prev_byte != ord('\\'):
                    print(f"Closing quote at byte {i}")
                    print(f"Context: {content[i-20:i+10]}")
                    # Show what follows
                    after = content[i:i+10]
                    print(f"After closing: {after}")
                    break
else:
    print("PiForz not found")
