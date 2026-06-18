WhatsApp Bridge QR / Pairing Code Status Report
=================================================
Date: 2026-06-10
Bridge port: 3000
Bridge source: C:\Users\Administrator\AppData\Local\hermes\hermes-agent\scripts\whatsapp-bridge\bridge.js

SESSION STATUS
--------------
Session location: D:\hermes\profiles\nichenexusglobal\whatsapp\session\creds.json
Registered: true
WhatsApp ID: 8619855653280:14@s.whatsapp.net (Pen's number)
LID: 206764809154731:14@lid
The session IS registered, but the bridge keeps generating QR codes because
the WebSocket connection fails (likely due to proxy/TUN mode issues).

WHAT I FOUND
------------
1. Bridge source code (bridge.js) is 246 lines - QR-based only
2. Endpoints available:
   - GET /health - status JSON
   - GET /qr - QR data as JSON (raw pairing URL string)
   - GET /qr/image - QR as base64 data URL
   - GET /messages - recent messages
   - POST /send - send message
   - POST /send-image - send image
3. NO pairing code endpoint exists in the current bridge
4. Baileys v6.7.23 DOES support requestPairingCode() - confirmed in node_modules
5. Existing QR data is saved in: D:\nichenexusglobal\qr_raw.txt
6. ASCII QR art is saved in: D:\nichenexusglobal\whatsapp_qr_code.txt
7. Bridge log (132K+ lines) shows continuous QR code regeneration

FILES CREATED
-------------
1. D:\nichenexusglobal\request_pairing.js
   - Standalone Node.js script to request a WhatsApp pairing code
   - Usage: node request_pairing.js <phone_number>
   - Example: node request_pairing.js 8619855653280
   - This bypasses the QR code requirement entirely
   - Outputs an 8-digit numeric code the user types in WhatsApp

2. D:\nichenexusglobal\generate_qr_png.py
   - Python script to generate QR PNG from existing raw data
   - Tries segno, qrcode, pyqrcode libraries in order
   - Output: D:\nichenexusglobal\whatsapp_connect_qr.png

3. D:\nichenexusglobal\whatsapp_qr_code.txt
   - Contains scannable ASCII QR art (use with another phone's camera)

4. D:\nichenexusglobal\qr_raw.txt
   - Contains raw QR pairing URL string

HOW TO USE THE PAIRING CODE SCRIPT
-----------------------------------
Step 1: Open a terminal (bash)
Step 2: cd C:/Users/Administrator/AppData/Local/hermes/hermes-agent/scripts/whatsapp-bridge
Step 3: run:
  node D:/nichenexusglobal/request_pairing.js 8619855653280
Step 4: The script will output an 8-digit pairing code
Step 5: On your phone:
  WhatsApp -> Settings -> Linked Devices -> Link a Device ->
  "Pair with phone number instead" -> enter the 8-digit code

HOW TO GENERATE QR PNG FROM RAW DATA
-------------------------------------
In a terminal with Python:
  python D:/nichenexusglobal/generate_qr_png.py

Or directly with pip + qrcode:
  pip install qrcode[pil]
  python -c "import qrcode; qrcode.make(open('D:/nichenexusglobal/qr_raw.txt').read().strip()).save('D:/nichenexusglobal/whatsapp_connect_qr.png')"

EXISTING QR RAW DATA
---------------------
The raw QR data is a WhatsApp pairing URL (beginning with "2@").
Length: ~234 characters
This is what gets encoded into the QR image for scanning.

TO RESTART THE BRIDGE WITH EXISTING SESSION
-------------------------------------------
If the session is still valid:
  bash D:\nichenexusglobal\restart-wa-bridge.sh

But note: the bridge.log shows the bridge keeps generating fresh QR codes
because the session was likely cleared during one of the restart cycles
(401/403 errors trigger session clearing in bridge.js lines 182-186).

The 408 (Request Timeout) errors in the log suggest the Clash proxy
TUN mode may need to be enabled for WebSocket traffic to work.
