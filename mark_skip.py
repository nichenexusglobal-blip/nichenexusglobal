#!/usr/bin/env python3
import json

with open('bullets_db.json', 'r') as f:
    db = json.load(f)

mark = {
    'LTE Groupe (Lamine Traoré Entreprise)': 'SKIP - 杂项服务公司，打井/灌溉/农机为主，发电机是副业。非目标客户。',
    'Freshtec Energy Zambia': 'SKIP - 南非母公司成熟分销链，卖一线品牌(Deye/Canadian/Pylontech)。不缺供应商。',
    'ABT Global Ventures Ltd': 'SKIP - Alaba电气商有自有工厂，自己直接从中国进口。无需中间商。',
    'Solar King': 'SKIP - 已有Portable Stations产品线，卖BLUETTI AC200L。已有供应商。'
}

for b in db['whatsapp_bullets']:
    if b['company'] in mark:
        b['status'] = 'no_match'
        b['notes'] = mark[b['company']]
        # Remove draft since we won't send
        if 'draft' in b:
            del b['draft']
        print(f"✗ Marked: {b['company']}")

db['last_updated'] = '2026-06-25'
with open('bullets_db.json', 'w') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)
print("Done")
