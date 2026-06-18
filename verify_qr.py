import subprocess, sys

# Install qrcode if needed
subprocess.check_call([sys.executable, "-m", "pip", "install", "qrcode[pil]"])

import qrcode
from PIL import Image
import os

path = "D:\\nichenexusglobal\\whatsapp_qr.png"
pairing_code = "4G6B47R2XXXVR2UAYSFPU5M6FF"

# Check file exists
if not os.path.exists(path):
    print("FILE NOT FOUND - generating new one")
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(pairing_code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path)
    print(f"Generated QR code at {path}")
else:
    print(f"File exists: {path}")
    
# Verify it's a valid PNG
img = Image.open(path)
print(f"Format: {img.format}")
print(f"Size: {img.size}")
print(f"Mode: {img.mode}")
print(f"File size: {os.path.getsize(path)} bytes")
print(f"Valid PNG: {img.format == 'PNG'}")
print("DONE")
