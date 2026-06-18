WhatsApp Bridge Restart - Investigation Summary
===============================================

1. SESSION STATUS
   - TWO session directories exist:
     a) C:\Users\Administrator\AppData\Local\hermes\whatsapp\session
        - FULL session state (creds.json + 50+ session files, device lists, LID mappings)
        - This is the session the bridge was originally using (from bridge.log)
     b) D:/hermes/profiles/nichenexusglobal/whatsapp/session/
        - Only creds.json (stub/partial - bridge_out.log shows it works though)
   - Both have valid authentication data
   - Device lists include: 8619855653280 (Pen), 8617825097029, 8618783977889,
     8618783977899, 8618818901401, 8613823701041, and others

2. BRIDGE LOG ANALYSIS (bridge.log - 12K+ lines)
   - Bridge was originally in self-chat mode, later switched to personal mode
   - Initial connections SUCCEEDED ("WhatsApp connected!") at timestamps ~1779692141491
   - Then got connection closed reason 428 (server-side close)
   - After reconnect: CONSTANT 408 (Request Timeout) reconnection loop lasting
     throughout the log -- bridge could not maintain WebSocket connection
   - Received messages from users before disconnect:
     * 8619855653280@s.whatsapp.net (Pen's number)
     * 134016602763445@lid (unknown LID contact)
     * 145019654635540@lid (unknown LID contact)
   - These were ignored due to self-chat mode originally

3. BRIDGE_OUT.LOG ANALYSIS (recent)
   - bridge_out.log shows a RECENT successful start:
     "WhatsApp bridge listening on port 3000 (mode: personal)"
     "Session stored in: D:/hermes/profiles/nichenexusglobal/whatsapp/session"
     "WhatsApp connected!"  <-- successful connection
   - But only 6 lines total - bridge terminated shortly after connecting
   - bridge_debug.log is empty (0 bytes) - no debug output captured

4. ARCHIVER.LOG ANALYSIS (1990 lines)
   - Continuous "Bridge unreachable" errors
   - WinError 10061 = "connection refused" (no process on port 3000)
   - Recent entries show timed out errors
   - Archiver keeps restarting via watchdog but cannot connect

5. ROOT CAUSE - WebSocket 408 Timeouts
   - WhatsApp uses WebSocket protocol
   - Clash proxy in system proxy mode only proxies HTTP(S), NOT WebSocket
   - Without Clash TUN mode enabled, WebSocket connections to WhatsApp servers
     time out (408 error)
   - This is a documented known issue (whatsapp-bridge-setup.md)
   - Each 408 is followed by "Reconnecting in 3s..." infinite loop
   - Bridge starts, connects briefly, then drops to 408 loop

6. FILES CREATED
   - D:/nichenexusglobal/restart-wa-bridge.sh - Comprehensive restart script with:
     * Kills processes on port 3000
     * Starts bridge with profile session path
     * Sets WHATSAPP_ALLOWED_USERS env var
     * Uses node v22 explicitly
     * Progressive health checks (3 retries)
     * Message polling on success
   - D:/nichenexusglobal/wa-bridge-analysis.md - This analysis

7. REQUIRED ACTION
   - Run the restart script: bash D:/nichenexusglobal/restart-wa-bridge.sh
   - If 408 errors continue, check Clash TUN mode is enabled
   - Clash Verge Rev -> Settings -> TUN Mode -> Enable
   - If session truly expired, QR re-pair needed via phone
