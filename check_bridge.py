"""
Check WhatsApp bridge status and try to extract QR code or pairing code.
"""
import socket
import urllib.request
import urllib.error
import json
import sys
import os
import subprocess
import re

def check_port(host, port):
    """Check if a port is open"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def http_get(url, timeout=5):
    """Simple HTTP GET"""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            return resp.status, data, dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers)
    except Exception as e:
        return None, str(e), {}

def check_bridge():
    print("=" * 60)
    print("WHATSAPP BRIDGE - QR CODE / PAIRING CODE CHECK")
    print("=" * 60)
    
    # Check if bridge is running
    port_open = check_port('127.0.0.1', 3000)
    print(f"\n[1] Port 3000 open: {port_open}")
    
    endpoints = [
        '/',
        '/qr',
        '/qrcode',
        '/status',
        '/health',
        '/api',
        '/api/status',
        '/login',
        '/pair',
        '/pairing',
        '/pairing-code',
        '/paircode',
        '/code',
        '/api/qr',
    ]
    
    for ep in endpoints:
        url = f'http://localhost:3000{ep}'
        status, data, headers = http_get(url)
        if status and status < 500:
            content_type = headers.get('Content-Type', '')
            size = len(data) if data else 0
            preview = ''
            if data:
                try:
                    preview = data[:200].decode('utf-8', errors='replace')
                except:
                    preview = f'<binary data {size} bytes>'
            print(f"\n  {url}")
            print(f"    Status: {status} | Content-Type: {content_type} | Size: {size}")
            print(f"    Preview: {preview[:150]}")
    
    if not port_open:
        print("\n[2] Bridge is NOT running. Checking for existing session data...")
        
        # Check the session directory
        session_dir = r"D:\hermes\profiles\nichenexusglobal\whatsapp\session"
        if os.path.exists(session_dir):
            files = os.listdir(session_dir)
            print(f"    Session files: {files}")
            
            # Check creds for registration status
            creds_path = os.path.join(session_dir, "creds.json")
            if os.path.exists(creds_path):
                with open(creds_path) as f:
                    try:
                        creds = json.load(f)
                        registered = creds.get('registered', False)
                        me = creds.get('me', {})
                        print(f"    Registered: {registered}")
                        print(f"    WhatsApp ID: {me}")
                    except:
                        print("    Could not parse creds.json")
        
        # Check existing QR raw data
        qr_raw = r"D:\nichenexusglobal\qr_raw.txt"
        if os.path.exists(qr_raw):
            with open(qr_raw) as f:
                raw = f.read().strip()
            print(f"\n[3] Existing QR raw data (first 60 chars): {raw[:60]}...")
            print(f"    Length: {len(raw)}")
            
            # Try to generate QR code
            try:
                import segno
                qr = segno.make(raw)
                out_path = r"D:\nichenexusglobal\whatsapp_connect_qr.png"
                qr.save(out_path, scale=10)
                print(f"    QR PNG generated: {out_path}")
            except ImportError:
                pass
            try:
                import qrcode
                qr_img = qrcode.make(raw)
                out_path = r"D:\nichenexusglobal\whatsapp_connect_qr.png"
                qr_img.save(out_path)
                print(f"    QR PNG generated (qrcode): {out_path}")
            except ImportError:
                pass
            try:
                import pyqrcode
                qr = pyqrcode.create(raw)
                out_path = r"D:\nichenexusglobal\whatsapp_connect_qr.png"
                qr.png(out_path, scale=10)
                print(f"    QR PNG generated (pyqrcode): {out_path}")
            except ImportError:
                print("    No QR library available in Python")
        
        print("\n[4] Checking bridge start script location...")
        bridge_dir = r"C:/Users/Administrator/AppData/Local/hermes/hermes-agent/scripts/whatsapp-bridge"
        if os.path.exists(bridge_dir):
            files = os.listdir(bridge_dir)
            print(f"    Bridge dir files: {files}")
            bridge_js = os.path.join(bridge_dir, "bridge.js")
            if os.path.exists(bridge_js):
                with open(bridge_js, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read(5000)
                # Look for pairing code patterns
                pairing_patterns = [
                    r'pair(?:ing)?[-_]?code',
                    r'pair(?:ing)?Code',
                    r'requestPairingCode',
                    r'pairNumber',
                    r'phoneNumber.*pair',
                    r'pair.*phone',
                ]
                for pat in pairing_patterns:
                    matches = re.findall(pat, content, re.IGNORECASE)
                    if matches:
                        print(f"    Found '{pat}' in bridge.js: {matches}")
                
                # Look for route definitions
                route_pattern = r"(app|router|server)\.(get|post|use)\s*\(['\"`](/[^'\"`]*)"
                routes = re.findall(route_pattern, content, re.IGNORECASE)
                if routes:
                    print(f"    Routes found in bridge.js:")
                    for r in routes:
                        print(f"      {r[1].upper()} {r[2]}")
    else:
        print("\n[2] Bridge IS running. Let's check the connection status...")

if __name__ == '__main__':
    check_bridge()
