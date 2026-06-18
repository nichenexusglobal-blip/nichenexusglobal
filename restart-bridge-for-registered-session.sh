#!/bin/bash
# Kill old WhatsApp bridge and restart with registered session

echo "=== Starting bridge restart $(date) ==="

# Kill all node processes (bridge only)
echo "Killing node processes..."
taskkill //F //IM node.exe 2>/dev/null || true

sleep 3

# Kill anything on port 3000
echo "Killing port 3000..."
# Find PID on port 3000
PID_3000=$(netstat -ano | grep ':3000 ' | grep LISTEN | awk '{print $5}' 2>/dev/null | head -1)
if [ -n "$PID_3000" ]; then
  taskkill //F //PID $PID_3000 2>/dev/null || true
fi

sleep 2

# Verify port is free
PORT_CHECK=$(netstat -ano | grep ':3000 ' | grep LISTEN | head -1)
echo "Port 3000 after kill: ${PORT_CHECK:-FREE}"

# Navigate to bridge directory
cd "C:/Users/Administrator/AppData/Local/hermes/hermes-agent/scripts/whatsapp-bridge" || {
  echo "ERROR: Cannot cd to bridge directory"
  exit 1
}

pwd
echo "Starting bridge with registered session..."

# Start bridge in background
nohup npx tsx src/index.ts \
  --session-dir "D:/hermes/profiles/nichenexusglobal/whatsapp/session" \
  --self-chat 0 \
  --bridge-port 3000 \
  >> D:/hermes/profiles/nichenexusglobal/whatsapp/bridge.log 2>&1 &

BRIDGE_PID=$!
echo "Bridge started with PID: $BRIDGE_PID"

sleep 15

echo "=== Checking bridge log after restart ==="
tail -5 D:/hermes/profiles/nichenexusglobal/whatsapp/bridge.log

echo "=== Checking port 3000 ==="
netstat -ano | grep ':3000 ' | grep LISTEN || echo "Port 3000: NOT LISTENING"

echo "=== Done $(date) ==="
