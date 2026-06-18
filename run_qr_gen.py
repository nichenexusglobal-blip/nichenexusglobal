#!/usr/bin/env python3
"""Standalone QR code generator for WhatsApp bridge pairing code.
Reads from qr_raw.txt and outputs whatsapp_qr.png.
Auto-installs dependencies if missing."""
import sys, os, subprocess

QR_RAW = r"D:\nichenexusglobal\qr_raw.txt"
QR_PNG = r"D:\nichenexusglobal\whatsapp_qr.png"

# Read raw pairing code
if not os.path.exists(QR_RAW):
    print("ERROR: qr_raw.txt not found")
    sys.exit(1)

with open(QR_RAW) as f:
    raw = f.read().strip()

if not raw:
    print("ERROR: qr_raw.txt is empty")
    sys.exit(1)

print(f"Read pairing code: {len(raw)} chars")

# Ensure qrcode[pil] is installed
try:
    import qrcode
    from PIL import Image
except ImportError:
    print("Installing qrcode[pil]...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "qrcode[pil]", "-q"])
    import qrcode
    from PIL import Image

# Generate QR code PNG
qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data(raw)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save(QR_PNG)
bytes_written = os.path.getsize(QR_PNG)
print(f"SUCCESS: QR code saved to {QR_PNG} ({bytes_written} bytes)")
