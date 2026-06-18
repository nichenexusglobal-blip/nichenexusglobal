#!/bin/bash
# WhatsApp Archiver Watchdog
# Checks if archiver is running, starts it if not

ARCHIVER_PID=$(ps aux 2>/dev/null | grep "whatsapp_archive.py --daemon" | grep -v grep | awk '{print $2}')

if [ -z "$ARCHIVER_PID" ]; then
    echo "[$(date)] Archiver not running. Starting..."
    cd /c/Users/Administrator/nichenexusglobal
    nohup python whatsapp_archive.py --daemon > /dev/null 2>&1 &
    echo "[$(date)] Archiver started"
else
    echo "[$(date)] Archiver running (PID $ARCHIVER_PID)"
fi
