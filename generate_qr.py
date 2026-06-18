#!/usr/bin/env python3
"""Generate WhatsApp Web pairing QR code PNG and verify it."""
import subprocess, sys, os

# Step 1: Install qrcode[pil]
print("Installing qrcode[pil]...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "qrcode[pil]"])
print("Installed.")

# Step 2: Generate QR code
import qrcode
from PIL import Image

pairing_code = "4G6B47R2XXXVR2UAYSFPU5M6FF"
out_path = "D:\\nichenexusglobal\\whatsapp_qr.png"

qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data(pairing_code)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save(out_path)
print(f"QR code saved to {out_path}")

# Step 3: Verify
img2 = Image.open(out_path)
assert img2.format == "PNG", "Not a valid PNG!"
print(f"Format: {img2.format}")
print(f"Size: {img2.size}")
print(f"Mode: {img2.mode}")
print(f"Bytes: {os.path.getsize(out_path)}")
print("SUCCESS: Valid QR code PNG generated and verified.")
