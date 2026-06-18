#!/usr/bin/env python3
"""Generate QR PNG from bridge's raw pairing data."""
import sys, os, json

QR_RAW = r"D:\nichenexusglobal\qr_raw.txt"
QR_PNG = r"D:\nichenexusglobal\whatsapp_qr.png"

# Read raw pairing code
if not os.path.exists(QR_RAW):
    print("STATUS=NO_QR_RAW")
    sys.exit(0)

with open(QR_RAW) as f:
    raw = f.read().strip()

if not raw:
    print("STATUS=QR_RAW_EMPTY")
    sys.exit(0)

# Generate QR PNG
try:
    import qrcode
    from PIL import Image
except ImportError:
    # Install if needed
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "qrcode[pil]", "-q"])
    import qrcode
    from PIL import Image

qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data(raw)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save(QR_PNG)

print(f"STATUS=OK data_len={len(raw)} png_bytes={os.path.getsize(QR_PNG)}")
sys.exit(0)
