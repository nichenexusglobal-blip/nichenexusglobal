#!/usr/bin/env python3
"""Write Genectra email draft - ask, don't pitch."""
import json

with open('bullets_db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# Find Genectra entry
for b in db['email_bullets']:
    if b['company'] == 'Genectra (Chile)':
        # Update with proper research data and new draft
        b['website'] = 'genectra.cl'
        b['products_sold'] = 'NOMAD Mini 300W, NOMAD Station 800W, Adventure 1200W, Freedom Solar 3600W, Titan Power 7200W - own brand power stations'
        b['market_position'] = 'Chilean solar generator company with own brand (NOMAD, ADVENTURE, FREEDOM, TITAN). Physical store in San Bernardo, Santiago. Also serves Argentina via genectra.com.'
        b['contact_source'] = 'Website: contacto@genectra.cl / WhatsApp +56 9 3250 7085 / Physical store San Bernardo'
        b['notes'] = 'Has own brand already. Potential OEM partner. Physical location: Pdte. Jorge Alessandri Rodriguez 9243, Bodega 13, San Bernardo. Previous WA contact June 7 - replied asking to email.'
        b['research_depth'] = 'verified_on_website'
        b['research_date'] = '2026-06-24'
        
        # NEW DRAFT - ask, don't pitch
        b['draft_email'] = (
            "Asunto: Consulta sobre su línea de productos\n\n"
            "Hola Genectra,\n\n"
            "Soy Pen de nichenexusglobal en Shenzhen, China. Hablamos por WhatsApp "
            "hace unas semanas y me pidieron enviar información a este correo.\n\n"
            "He visto su sitio web — la línea NOMAD, ADVENTURE, FREEDOM y TITAN "
            "que tienen para Chile y Argentina. Productos con buena presencia.\n\n"
            "Nosotros somos una empresa de sourcing en Shenzhen. Trabajamos con "
            "fábricas OEM de estaciones LiFePO4. No fabricamos nosotros mismos, "
            "pero conocemos bien las fábricas y podemos ayudarlos a encontrar el "
            "producto correcto.\n\n"
            "Para poder enviarles información relevante y no genérica, quisiera "
            "entender mejor qué están buscando:\n\n"
            "1. ¿Están buscando un nuevo modelo para agregar a su línea actual, "
            "o reemplazar algún producto existente?\n"
            "2. ¿Qué capacidad y wattaje les interesa?\n"
            "3. ¿Qué certificaciones necesitan para el mercado chileno?\n"
            "4. ¿Qué volumen mensual estimado manejan?\n\n"
            "Con eso puedo buscar opciones concretas de fábricas que cumplan "
            "con sus requisitos.\n\n"
            "Quedo atento a su respuesta.\n\n"
            "Saludos,\n"
            "Pen\n"
            "nichenexusglobal.com"
        )
        
        print("✅ Genectra draft updated")
        print()
        print(b['draft_email'])
        print()
        print(f"Products: {b['products_sold']}")
        print(f"Position: {b['market_position']}")
        break

with open('bullets_db.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("✅ bullets_db.json saved")
