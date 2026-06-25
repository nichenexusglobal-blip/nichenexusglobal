#!/usr/bin/env python
"""Send product info email to Voltaris Colombia"""

import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

env_path = r'C:\nichenexusglobal\.env'
password = None
with open(env_path, 'r') as f:
    for pwline in f:
        pwline = pwline.strip()
        if not pwline.startswith('NICHE_EMAIL_PASSWORD='):
            continue
        password = pwline.split('=', 1)[1].strip().strip("'\\\"")
        break

if not password:
    print("FAIL: NICHE_EMAIL_PASSWORD not found")
    exit(1)

smtp_host = "smtp.exmail.qq.com"
smtp_port = 465
sender = "pen@nichenexusglobal.com"
recipient = "ventas@voltaris.co"

msg = MIMEMultipart("alternative")
msg["From"] = f"Pen | nichenexusglobal <{sender}>"
msg["To"] = recipient
msg["Subject"] = "Información de productos LiFePO4 - estaciones de energía portátiles"

text_body = """Hola Voltaris,

Pen de nichenexusglobal. Disculpa la demora en responder.

Somos una empresa de sourcing en Shenzhen, China. Trabajamos con fabricas OEM de estaciones de energia portatiles LiFePO4.

Nuestra gama de referencia FOB:
- 1000Wh/1000W ~ USD 145
- 2000Wh/1200W ~ USD 298
- 3600Wh/2200W ~ USD 620
- 5400Wh/5000W ~ USD 898

Certificacion CE/FCC. Ciclos 6000+. Posibilidad de marca propia (OEM/ODM).

Si les interesa tener una linea complementaria a EcoFlow, Bluetti y las otras marcas que distribuyen, con gusto les envio el catalogo completo con especificaciones y fotos reales.

Saludos,
Pen
nichenexusglobal.com"""

html_body = """<html><body style="font-family:Arial,sans-serif;color:#333;">
<p>Hola Voltaris,</p>
<p>Pen de <a href="https://nichenexusglobal.com">nichenexusglobal</a>. Disculpa la demora en responder.</p>
<p>Somos una empresa de sourcing en Shenzhen, China. Trabajamos con fabricas OEM de estaciones de energia portatiles LiFePO4.</p>
<p>Nuestra gama de referencia FOB:</p>
<table style="border-collapse:collapse;width:100%;max-width:400px;">
<tr style="background:#f5f5f5;"><td style="padding:8px;border:1px solid #ddd;">1000Wh/1000W</td><td style="padding:8px;border:1px solid #ddd;">~USD 145</td></tr>
<tr><td style="padding:8px;border:1px solid #ddd;">2000Wh/1200W</td><td style="padding:8px;border:1px solid #ddd;">~USD 298</td></tr>
<tr style="background:#f5f5f5;"><td style="padding:8px;border:1px solid #ddd;">3600Wh/2200W</td><td style="padding:8px;border:1px solid #ddd;">~USD 620</td></tr>
<tr><td style="padding:8px;border:1px solid #ddd;">5400Wh/5000W</td><td style="padding:8px;border:1px solid #ddd;">~USD 898</td></tr>
</table>
<br>
<p>Certificacion CE/FCC. Ciclos 6000+. Posibilidad de marca propia (OEM/ODM).</p>
<p>Si les interesa tener una linea complementaria a EcoFlow, Bluetti y las otras marcas que distribuyen, con gusto les envio el catalogo completo con especificaciones y fotos reales.</p>
<br>
<p>Saludos,<br>Pen<br><a href="https://nichenexusglobal.com">nichenexusglobal.com</a></p>
</body></html>"""

msg.attach(MIMEText(text_body, "plain"))
msg.attach(MIMEText(html_body, "html"))

try:
    with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as server:
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())
    print(f"SUCCESS: Email sent to {recipient}")
except Exception as e:
    print(f"FAIL: {e}")
    exit(1)
