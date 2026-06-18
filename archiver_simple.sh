#!/bin/bash
# Simple WhatsApp message archiver - polls bridge, saves to JSONL
# More reliable than the Python daemon mode
BRIDGE="http://127.0.0.1:3000"
DIR="/c/Users/Administrator/nichenexusglobal"
FILE="$DIR/whatsapp_messages.jsonl"
LOG="$DIR/archiver.log"

echo "[$(date)] Archiver started" >> "$LOG"

while true; do
  result=$(curl -s --max-time 10 "$BRIDGE/messages" 2>/dev/null)
  if [ $? -eq 0 ] && [ "$result" != "[]" ] && [ -n "$result" ]; then
    echo "$result" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data:
    for msg in data:
        entry = {
            'timestamp': msg.get('timestamp', ''),
            'chat_id': msg.get('chatId', ''),
            'sender_id': msg.get('senderId', ''),
            'sender_name': msg.get('senderName', msg.get('pushName', '')),
            'body': msg.get('body', ''),
            'message_id': msg.get('id', ''),
            'from_me': msg.get('fromMe', False),
        }
        print(json.dumps(entry, ensure_ascii=False))
" >> "$FILE" 2>> "$LOG"
    count=$(echo "$result" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))")
    echo "[$(date)] Stored $count messages" >> "$LOG"
  fi
  sleep 3
done
