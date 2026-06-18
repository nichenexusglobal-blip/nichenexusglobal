"""Generate QR code PNG from existing raw QR data."""
import sys
import os

QR_RAW = r"D:\nichenexusglobal\qr_raw.txt"
QR_PNG = r"D:\nichenexusglobal\whatsapp_connect_qr.png"

if not os.path.exists(QR_RAW):
    print(f"ERROR: {QR_RAW} not found")
    sys.exit(1)

with open(QR_RAW) as f:
    qr_data = f.read().strip()

if not qr_data:
    print("ERROR: QR data is empty")
    sys.exit(1)

print(f"Raw QR data length: {len(qr_data)} chars")
print(f"Raw QR data (first 60): {qr_data[:60]}...")

# Try different QR libraries
for lib_name, make_fn in [
    ("segno", lambda d: __import__('segno').make(d)),
    ("qrcode", lambda d: __import__('qrcode').make(d)),
    ("pyqrcode", lambda d: __import__('pyqrcode').create(d)),
]:
    try:
        qr = make_fn(qr_data)
        if lib_name == "segno":
            qr.save(QR_PNG, scale=10)
        elif lib_name == "qrcode":
            qr.save(QR_PNG)
        elif lib_name == "pyqrcode":
            qr.png(QR_PNG, scale=10)
        print(f"SUCCESS: QR PNG saved to {QR_PNG} using {lib_name}")
        print(f"File size: {os.path.getsize(QR_PNG)} bytes")
        sys.exit(0)
    except ImportError:
        print(f"  {lib_name} not available, trying next...")
        continue
    except Exception as e:
        print(f"  {lib_name} failed: {e}")
        continue

print("ERROR: No QR library available. Install one:")
print("  pip install qrcode[pil]")
print("  pip install segno")
print("  pip install pyqrcode pypng")
sys.exit(1)
