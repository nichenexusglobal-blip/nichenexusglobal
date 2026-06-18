@echo off
REM Start wago-api (whatsmeow bridge) standalone
set ALL_PROXY=socks5://127.0.0.1:7897
set PORT=3003
set SESSIONS_PATH=C:\nichenexusglobal\wago-api\sessions
set BASE_WEBHOOK_URL=http://127.0.0.1:3000/webhook
set ENABLE_WEBHOOK=true
set AUTO_START_SESSIONS=true
set LOG_LEVEL=warn

cd /d C:\nichenexusglobal\wago-api
start /B wago-api.exe > wago-api.log 2>&1
echo wago-api started on port 3003
