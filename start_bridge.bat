@echo off
cd /d C:\Users\leon/AppData/Local/hermes/hermes-agent/scripts/whatsapp-bridge
set JSONL_PATH=C:/nichenexusglobal/whatsapp_messages.jsonl
set WAGO_BIN=C:/nichenexusglobal\wago-api\wago-api.exe
node bridge.js
