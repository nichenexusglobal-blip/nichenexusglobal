"""Analyze WhatsApp messages log."""
import json
import os

MSG_FILE = r"C:\nichenexusglobal\whatsapp_messages.jsonl"
LAST_MSG_FILE = r"C:\nichenexusglobal\wago-api\.last_wa_msg"

# Check file timestamps
print("=== File info ===")
print(f"last_wa_msg mtime: {os.path.getmtime(LAST_MSG_FILE) if os.path.exists(LAST_MSG_FILE) else 'N/A'}")
print(f"whatsapp_messages.jsonl mtime: {os.path.getmtime(MSG_FILE)}")
print(f"whatsapp_messages.jsonl size: {os.path.getsize(MSG_FILE)} bytes")

# Read the last known marker
last_known = 0
if os.path.exists(LAST_MSG_FILE):
    with open(LAST_MSG_FILE) as f:
        last_known = int(f.read().strip())

# Read all lines
with open(MSG_FILE, encoding="utf-8") as f:
    lines = f.readlines()

total_lines = len(lines)
print(f"\nTotal lines: {total_lines}")
print(f"Last known marker: {last_known}")
print(f"New lines since marker: {total_lines - last_known}")

# Find incoming messages (not from me)
incoming = []
new_incoming = []

for i, line in enumerate(lines):
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
    except:
        continue
    
    if d.get("event") == "message" and not d.get("data", {}).get("isFromMe", True):
        data = d.get("data", {})
        msg = {
            "body": data.get("body", ""),
            "sender": data.get("sender", ""),
            "pushName": data.get("pushName", ""),
            "timestamp": data.get("timestamp", 0),
            "received_at": d.get("_received_at", ""),
            "line": i + 1
        }
        incoming.append(msg)
        if i + 1 > last_known:
            new_incoming.append(msg)

print(f"\n=== INCOMING MESSAGES ===")
print(f"Total incoming (ever): {len(incoming)}")

# Find contacts info from the DB contacts - already printed earlier

# Show last 10 incoming messages
if incoming:
    print(f"\nLast 10 incoming messages:")
    for msg in incoming[-10:]:
        print(f"  [{msg['received_at']}] {msg['pushName']}: \"{msg['body'][:100]}\" (line {msg['line']})")

print(f"\n=== NEW INCOMING (since marker {last_known}) ===")
if new_incoming:
    print(f"  Count: {len(new_incoming)}")
    for msg in new_incoming:
        print(f"  [{msg['received_at']}] {msg['pushName']}: \"{msg['body'][:100]}\" (line {msg['line']})")
else:
    print("  None")

# Also check all unique contacts who have messaged
contacts = set()
for msg in incoming:
    contacts.add((msg['sender'], msg['pushName']))
print(f"\n=== ACTIVE CONTACTS (incoming only) ===")
for sender, name in sorted(contacts):
    print(f"  {name} ({sender})")
