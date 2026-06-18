#!/usr/bin/env python3
"""WhatsApp Bridge Status Report - no subprocess calls, safe to read"""
import os, json, sys

def check_bridge():
    report = []
    report.append("=" * 60)
    report.append("WHATSAPP BRIDGE STATUS REPORT")
    report.append("=" * 60)
    
    # 1. Session status
    session_dir = "D:/hermes/profiles/nichenexusglobal/whatsapp/session"
    creds_path = os.path.join(session_dir, "creds.json")
    report.append(f"\n[SESSION] Dir: {session_dir}")
    report.append(f"[SESSION] Exists: {os.path.isdir(session_dir)}")
    
    if os.path.isfile(creds_path):
        with open(creds_path) as f:
            creds = json.load(f)
        registered = creds.get("registered", False)
        me = creds.get("me", {})
        phone = me.get("id", "unknown") if me else "unknown"
        report.append(f"[SESSION] Registered: {registered}")
        report.append(f"[SESSION] Phone: {phone}")
    else:
        report.append("[SESSION] creds.json NOT FOUND - need to pair!")
    
    # 2. Bridge log
    bridge_log = "D:/hermes/profiles/nichenexusglobal/whatsapp/bridge.log"
    if os.path.isfile(bridge_log):
        with open(bridge_log) as f:
            lines = f.readlines()
        tail = lines[-20:] if len(lines) >= 20 else lines
        report.append(f"\n[BRIDGE LOG] ({len(lines)} lines total, last {len(tail)}):")
        for l in tail:
            report.append(f"  {l.rstrip()}")
    else:
        report.append("\n[BRIDGE LOG] No bridge.log found")
    
    # 3. Archived messages
    msg_file = "D:/nichenexusglobal/whatsapp_messages.jsonl"
    if os.path.isfile(msg_file):
        with open(msg_file) as f:
            msgs = [l for l in f if l.strip()]
        report.append(f"\n[MESSAGES ARCHIVE] ({len(msgs)} messages stored)")
        for m in msgs[-5:]:
            try:
                data = json.loads(m)
                report.append(f"  - [{data.get('timestamp','?')}] {data.get('sender_name','?')}: {data.get('body','?')[:80]}")
            except:
                pass
    else:
        report.append("\n[MESSAGES ARCHIVE] No messages archive found")
    
    # 4. whatsapp_messages directory
    msg_dir = "D:/nichenexusglobal/whatsapp_messages"
    if os.path.isdir(msg_dir):
        files = os.listdir(msg_dir)
        report.append(f"\n[ARCHIVE DIR] {len(files)} files found")
        for f in sorted(files)[-5:]:
            fpath = os.path.join(msg_dir, f)
            fsize = os.path.getsize(fpath)
            report.append(f"  - {f} ({fsize} bytes)")
    else:
        report.append("\n[ARCHIVE DIR] Directory does not exist")
    
    # 5. bridge_out.log
    if os.path.isfile("D:/nichenexusglobal/bridge_out.log"):
        with open("D:/nichenexusglobal/bridge_out.log") as f:
            lines = [l for l in f if l.strip()]
        report.append(f"\n[BRIDGE OUT LOG] ({len(lines)} lines):")
        for l in lines:
            report.append(f"  {l}")
    
    report.append("\n" + "=" * 60)
    report.append("RECOMMENDATION")
    report.append("=" * 60)
    
    if registered:
        report.append("Session is registered. To start the bridge, run:")
        report.append("  bash D:/nichenexusglobal/restart-wa-bridge.sh")
        report.append("Then check: curl -s http://localhost:3000/health")
    else:
        report.append("Session NOT registered. Need to generate QR code and scan with phone.")
        report.append("  node D:/nichenexusglobal/qr_gen.js")
    
    return "\n".join(report)

if __name__ == "__main__":
    print(check_bridge())
