"""
WhatsApp Bridge QR Code Generator
Starts bridge.js, monitors log for QR data, generates QR PNG.
"""
import subprocess
import time
import os
import sys
import re

BRIDGE_JS = r"D:\nichenexusglobal\bridge.js"
BRIDGE_LOG = r"D:\nichenexusglobal\bridge.log"
QR_RAW = r"D:\nichenexusglobal\qr_raw.txt"
QR_PNG = r"D:\nichenexusglobal\whatsapp_connect_qr.png"
WORK_DIR = r"D:\nichenexusglobal"
TIMEOUT = 25

def main():
    print("[*] Starting bridge.js in background...")

    # Clear old log
    if os.path.exists(BRIDGE_LOG):
        os.remove(BRIDGE_LOG)

    proc = subprocess.Popen(
        ["node", BRIDGE_JS],
        cwd=WORK_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    start_time = time.time()
    qr_data = None

    try:
        while time.time() - start_time < TIMEOUT:
            line = proc.stdout.readline()
            if not line:
                time.sleep(0.1)
                continue

            line = line.strip()
            print(f"[bridge] {line[:120]}")

            # Check for "QR data:" in the line
            if "QR data:" in line:
                # Parse out the QR data - after "QR data:"
                match = re.search(r"QR data:\s*(.+)", line, re.IGNORECASE)
                if match:
                    qr_data = match.group(1).strip()
                    print(f"[*] Found QR data: {qr_data[:80]}...")
                    break

            # Also check bridge.log if it exists
            if os.path.exists(BRIDGE_LOG):
                try:
                    with open(BRIDGE_LOG, "r") as f:
                        for l in f:
                            if "QR data:" in l:
                                m = re.search(r"QR data:\s*(.+)", l, re.IGNORECASE)
                                if m:
                                    qr_data = m.group(1).strip()
                                    print(f"[*] Found QR data in log: {qr_data[:80]}...")
                                    break
                except:
                    pass

            if qr_data:
                break

        if not qr_data:
            # Final check of bridge.log
            if os.path.exists(BRIDGE_LOG):
                with open(BRIDGE_LOG, "r") as f:
                    for l in f:
                        if "QR data:" in l:
                            m = re.search(r"QR data:\s*(.+)", l, re.IGNORECASE)
                            if m:
                                qr_data = m.group(1).strip()
                                print(f"[*] Found QR data in final log check: {qr_data[:80]}...")
                                break

        if not qr_data:
            print("[!] No QR data found within timeout.")
            proc.terminate()
            return 1

        # Save raw QR data
        with open(QR_RAW, "w") as f:
            f.write(qr_data)
        print(f"[*] Saved QR data to {QR_RAW}")

        # Generate QR PNG
        print("[*] Generating QR PNG...")
        try:
            import segno
            qr = segno.make(qr_data)
            qr.save(QR_PNG, scale=10)
            print(f"[*] QR PNG saved to {QR_PNG} using segno")
        except ImportError:
            print("[!] segno not available, trying qrcode...")
            try:
                import qrcode
                qr_img = qrcode.make(qr_data)
                qr_img.save(QR_PNG)
                print(f"[*] QR PNG saved to {QR_PNG} using qrcode")
            except ImportError:
                print("[!] qrcode also not available, trying pyqrcode + pypng...")
                try:
                    import pyqrcode
                    qr = pyqrcode.create(qr_data)
                    qr.png(QR_PNG, scale=10)
                    print(f"[*] QR PNG saved to {QR_PNG} using pyqrcode")
                except ImportError:
                    print("[!] No QR library available. Writing raw data only.")
                    return 1

        return 0

    except KeyboardInterrupt:
        print("[!] Interrupted.")
        proc.terminate()
        return 1
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except:
                proc.kill()

if __name__ == "__main__":
    sys.exit(main())
