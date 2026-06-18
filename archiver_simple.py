#!/usr/bin/env python3
"""WhatsApp Archiver v3 - uses subprocess curl to avoid Windows port exhaustion."""
import subprocess, json, os, sys, time
from datetime import datetime, timezone, timedelta

DIR = os.path.expanduser("~/nichenexusglobal")
FILE = os.path.join(DIR, "whatsapp_messages.jsonl")
LOG_FILE = os.path.join(DIR, "archiver.log")
TZ8 = timezone(timedelta(hours=8))
LAST_ID_FILE = os.path.join(DIR, ".archiver_last_id")

def log(msg):
    ts = datetime.now(TZ8).strftime("%H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}", flush=True)

def load_last_id():
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE) as f:
            return f.read().strip()
    return None

def save_last_id(msg_id):
    with open(LAST_ID_FILE, "w") as f:
        f.write(msg_id)

log("Archiver started (curl-based)")
last_id = load_last_id()
if last_id:
    log(f"Resuming from: {last_id[:20]}...")

empty_count = 0

while True:
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "10", "http://127.0.0.1:3000/messages"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            empty_count += 1
            if empty_count % 10 == 0 and empty_count <= 30:
                log(f"Curl exit code {result.returncode} ({empty_count}x)")
            time.sleep(30)
            continue
        
        output = result.stdout.strip()
        if not output or output == "[]":
            empty_count += 1
            time.sleep(30)
            continue
        
        messages = json.loads(output)
        if not messages:
            empty_count += 1
            time.sleep(30)
            continue
        
        new_count = 0
        for msg in messages:
            msg_id = msg.get("id", "")
            if last_id and msg_id and msg_id <= last_id:
                continue
            entry = {
                "timestamp": datetime.now(TZ8).isoformat(),
                "chat_id": msg.get("chatId", ""),
                "sender_id": msg.get("senderId", ""),
                "sender_name": msg.get("senderName", msg.get("pushName", "")),
                "body": msg.get("body", ""),
                "message_id": msg_id,
                "from_me": msg.get("fromMe", False),
            }
            with open(FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            if msg_id:
                last_id = msg_id
                save_last_id(msg_id)
            new_count += 1
        
        log(f"Stored {new_count} messages")
        empty_count = 0
        time.sleep(30)
    except Exception as e:
        log(f"Error: {e}")
        time.sleep(30)
