#!/usr/bin/env python
"""Monitor qr_raw.txt and generate QR PNG when data appears."""
import time
import os
import sys

QR_RAW = r"D:\nichenexusglobal\qr_raw.txt"
QR_PNG = r"D:\nichenexusglobal\whatsapp_qr.png"

def generate_png(qr_text):
    """Generate QR code PNG from text data."""
    try:
        import qrcode
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(qr_text)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        img.save(QR_PNG)
        print(f"QR PNG saved to {QR_PNG}")
        return True
    except ImportError:
        pass

    try:
        # Try with pillow
        import qrcode
        import qrcode.image.pil
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(qr_text)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        img.save(QR_PNG)
        print(f"QR PNG saved to {QR_PNG}")
        return True
    except ImportError:
        pass

    # Fallback: write HTML with QR via Google Charts API
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>WhatsApp QR</title>
<style>
body {{ display:flex; justify-content:center; align-items:center; min-height:100vh; background:#fff; }}
img {{ max-width:500px; }}
</style></head><body>
<img src="https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={qr_text}" alt="QR Code">
</body></html>"""
    with open(r"D:\nichenexusglobal\whatsapp_qr.html", "w") as f:
        f.write(html)
    print(f"QR HTML saved with API fallback")
    return True

def main():
    print(f"Monitoring {QR_RAW} for QR data...")
    last_size = 0
    while True:
        if os.path.exists(QR_RAW):
            size = os.path.getsize(QR_RAW)
            if size > 0 and size != last_size:
                with open(QR_RAW, "r") as f:
                    qr_data = f.read().strip()
                if qr_data:
                    print(f"QR data found! ({len(qr_data)} chars)")
                    generate_png(qr_data)
                    last_size = size
        time.sleep(2)

if __name__ == "__main__":
    main()
