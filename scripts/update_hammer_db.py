#!/usr/bin/env python3
"""Update hammer_db.json with new findings from email + PDF analysis"""
import json

with open('C:\\nichenexusglobal\\hammer_db.json', 'r') as f:
    db = json.load(f)

updates = []

# 1. ALLPOWERS - update with full catalog data from Nina's PDF
allpowers_entry = None
for h in db.get('verified_suppliers', {}).get('hammers', []):
    if h.get('name') == 'ALLPOWERS':
        allpowers_entry = h
        break

if allpowers_entry:
    allpowers_entry['specs'] = {
        'P1800_1024Wh': '1800W/1024Wh/LFP',
        'P300_256Wh': '300W/256Wh/LFP', 
        'P100_99Wh': '100W/99.2Wh/LFP',
        'R4000Pro_3456Wh': '4000W/3456Wh/LFP',
        'R3500_3168Wh': '3500W/3168Wh/LFP',
        'R2500_2016Wh': '2500W/2016Wh/LFP',
        'R1500LITE_1056Wh': '1600W/1056Wh/LFP',
        'R600_299Wh': '600W/299Wh/LFP',
        'B3000_3168Wh': 'expandable battery pack 3168Wh/LFP'
    }
    allpowers_entry['catalog_models'] = ['P1800','P300','P100','R4000Pro','R3500','R2500','R1500LITE','R600','B3000']
    allpowers_entry['catalog_source'] = 'Nina/ALLPOWERS Product Catalog 2026.pdf'
    allpowers_entry['notes'] = 'Full catalog confirmed (Nina). Only R600 FOB price known ($150). Need to request FOB pricing from Nina for other models.'
    allpowers_entry['data_quality'] = 'C'
    updates.append('ALLPOWERS: expanded to 9 models from Nina catalog')

# 2. Anern - update with PI details
anern_entry = None
for h in db.get('verified_suppliers', {}).get('hammers', []):
    if h.get('name') == 'Anern Energy':
        anern_entry = h
        break

if anern_entry:
    # Update product naming from PI
    anern_entry['pi_confirmed'] = {
        'PI_ref': 'ANSD240605-LU',
        'PI_date': '2026-06-05',
        'payment_terms': '30% deposit, 70% before shipment',
        'port': 'FOB Guangzhou',
        'MPSG-N500': {'w': 500, 'wh': 600, 'fob_qty_100': 199, 'socket': 'UK Type G'},
        'MPSG-E1200': {'w': 1200, 'wh': 1280, 'fob_qty_100': 205, 'socket': 'UK Type G'},
        'MPSG-E2000': {'w': 2000, 'wh': 2560, 'fob_qty_50': 323, 'socket': 'UK Type G'}
    }
    updates.append('Anern: PI confirmed - 3 models, 30% deposit, FOB Guangzhou, UK socket')

# 3. Market index update
mi = db.get('verified_suppliers', {}).get('market_index', {})
# We now have shipping costs to these markets from Pecron Chris
mi['Kenya'] = list(set(mi.get('Kenya', []) + ['Pecron', 'Anern Energy', 'MECO Power']))
mi['Philippines'] = list(set(mi.get('Philippines', []) + ['Pecron']))
mi['UAE_Dubai'] = list(set(mi.get('UAE_Dubai', []) + ['Pecron']))
updates.append('Market index: added MECO Power to Kenya')

# 4. Update meta
db['meta']['last_updated'] = '2026-06-21'
db['meta']['total_hammers'] = len(db.get('categories', {}).get('portable_power_1000w', {}).get('hammers', [])) + \
                               len(db.get('categories', {}).get('portable_power_2000w', {}).get('hammers', [])) + \
                               len(db.get('verified_suppliers', {}).get('hammers', []))

with open('C:\\nichenexusglobal\\hammer_db.json', 'w') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("✅ hammer_db.json 更新完成！")
for u in updates:
    print(f"  • {u}")
