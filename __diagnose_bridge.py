"""Diagnose WhatsApp bridge status - safe, no subprocess"""
import os, json

# 1. Check session files
session_dir = "D:/hermes/profiles/nichenexusglobal/whatsapp/session"
files = os.listdir(session_dir) if os.path.isdir(session_dir) else []
print(f"Session files ({len(files)}): {files[:5]}...")
print(f"Has creds.json: {os.path.isfile(os.path.join(session_dir, 'creds.json'))}")

# 2. Read creeds.json basic status
if os.path.isfile(os.path.join(session_dir, 'creds.json')):
    with open(os.path.join(session_dir, 'creds.json')) as f:
        creds = json.load(f)
    print(f"Registered: {creds.get('registered', 'N/A')}")
    print(f"ServerToken present: {'serverToken' in creds and bool(creds.get('serverToken'))}")

# 3. Check bridge logs
for logfile in ["bridge_debug.log", "bridge_out.log"]:
    path = f"D:/nichenexusglobal/{logfile}"
    if os.path.isfile(path):
        with open(path) as f:
            lines = f.readlines()
        tail = lines[-5:] if len(lines) >= 5 else lines
        print(f"\n--- {logfile} (last {len(tail)} of {len(lines)} lines) ---")
        for l in tail:
            print(l.rstrip())

# 4. Check .archiver.pid
pid_path = "D:/nichenexusglobal/.archiver.pid"
if os.path.isfile(pid_path):
    with open(pid_path) as f:
        print(f"\nArchiver PID: {f.read().strip()}")
else:
    print("\nNo .archiver.pid - archiver not running")
