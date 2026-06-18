@echo off
REM Start Hermes Gateway (auto-start after login)
REM This starts the gateway which will launch bridge-wago.js -> wago-api
cd /d C:\Users\leon\AppData\Local\hermes
hermes gateway run
