#!/usr/bin/env python3
"""Send Genectra email via Tencent Enterprise Mail SMTP."""
import smtplib, ssl, json, sys
sys.path.insert(0, '/c/nichenexusglobal')
from pwd_loader import get_pwd

PASSWORD = get_pwd()
FROM = "pen@nichenexusglobal.com"
TO = "contacto@genectra.cl"
SUBJECT = "Consulta sobre su línea de productos"

BODY = """Hola Genectra,

Soy Pen de nichenexusglobal en Shenzhen, China. Hablamos por WhatsApp hace unas semanas y me pidieron enviar información a este correo.

He visto su sitio web — la línea NOMAD, ADVENTURE, FREEDOM y TITAN que tienen para Chile y Argentina. Productos con buena presencia.

Nosotros somos una empresa de sourcing en Shenzhen. Trabajamos con fábricas OEM de estaciones LiFePO4. No fabricamos nosotros mismos, pero conocemos bien las fábricas y podemos ayudarlos a encontrar el producto correcto.

Para poder enviarles información relevante y no genérica, quisiera entender mejor qué están buscando:

1. ¿Están buscando un nuevo modelo para agregar a su línea actual, o reemplazar algún producto existente?
2. ¿Qué capacidad y wattaje les interesa?
3. ¿Qué certificaciones necesitan para el mercado chileno?
4. ¿Qué volumen mensual estimado manejan?

Con eso puedo buscar opciones concretas de fábricas que cumplan con sus requisitos.

Quedo atento a su respuesta.

Saludos,
Pen
nichenexusglobal.com"""

from email.mime.text import MIMEText

msg = MIMEText(BODY, "plain", "utf-8")
msg["From"] = f"Pen <{FROM}>"
msg["To"] = TO
msg["Subject"] = SUBJECT

context = ssl.create_default_context()

# Tencent Enterprise Mail SMTP - port 465
try:
    with smtplib.SMTP_SSL("smtp.exmail.qq.com", 465, context=context) as server:
        server.ehlo()
        server.login(FROM, PASSWORD)
        server.sendmail(FROM, [TO], msg.as_string())
    print(f"✅ Email sent to {TO}")
except Exception as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

# Update DB
with open('bullets_db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)
for b in db['email_bullets']:
    if b['company'] == 'Genectra (Chile)':
        b['sent'] = True
        b['sent_channel'] = 'email'
        b['sent_date'] = '2026-06-24'
        break
with open('bullets_db.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)
print("✅ bullets_db.json updated")
