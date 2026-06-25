#!/usr/bin/env python3
import json

with open('bullets_db.json', 'r') as f:
    db = json.load(f)

# Remove draft from Solar King (not a match - sells portable stations)
# Add/update drafts for the 3 correct bullets
drafts = {
    'LTE Groupe (Lamine Traoré Entreprise)': 
        "Bonjour l'équipe LTE 👋\n\nVous êtes actifs dans l'énergie, l'hydraulique et l'agricole en Côte d'Ivoire et dans la sous-région — avec une gamme qui inclut groupes électrogènes, panneaux solaires et batteries.\n\nNous travaillons avec des usines qui produisent des stations d'énergie portables LiFePO4. C'est un complément intéressant pour une entreprise qui vend déjà des solutions énergétiques : pas de bruit, pas de fumée, zéro carburant.\n\nPour référence, une station 1280Wh/1200W à $205 FOB. Certification CE/FCC. Marque blanche possible.\n\nSi vous voulez voir le catalogue, dites-le moi.\n\nPen",
    
    'Freshtec Energy Zambia':
        "Hi Freshtec team 👋\n\nYou distribute Deye inverters, Canadian Solar panels, lithium batteries and solar accessories from Lusaka. Clean product range for installers.\n\nWe work with factories producing LiFePO4 portable power stations — could be a useful add-on for your installer network.\n\nFor reference, a 1280Wh/1200W unit at $205 FOB. CE/FCC certified. MOQ flexible.\n\nWant me to send the specs?\n\nPen",
    
    'ABT Global Ventures Ltd':
        "Hi ABT Global team 👋\n\nYou sell electrical products, solar inverters and batteries from your Alaba Market showroom, with your own factory in Ogun State.\n\nWe work with factories that produce LiFePO4 portable power stations — could complement your existing electrical and solar range nicely.\n\nFor reference, a 1280Wh/1200W unit at $205 FOB. CE/FCC certified. MOQ flexible.\n\nWant to see what we have?\n\nPen"
}

# Remove drafts from non-selected bullets
for b in db['whatsapp_bullets']:
    if b['company'] == 'Solar King':
        if 'draft' in b:
            del b['draft']
            print(f"Removed draft from Solar King (not a match)")
    elif b['company'] in drafts:
        b['draft'] = drafts[b['company']]
        print(f"✓ Updated draft for {b['company']}")

db['last_updated'] = '2026-06-25'
with open('bullets_db.json', 'w') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)
print("Done")
