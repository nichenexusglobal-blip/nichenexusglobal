#!/usr/bin/env python3
import json
db = json.load(open('bullets_db.json'))
wa = db['whatsapp_bullets']
unsent = [b for b in wa if b.get('status') in ('verified','researched') or b.get('sent') == False]
print(f'Total WA bullets: {len(wa)}')
print(f'Unsent: {len(unsent)}')
for i,b in enumerate(unsent):
    print(f'  {i+1}. {b["company"]} ({b["market"]}) WA:{b.get("whatsapp","?")} status:{b.get("status","?")}')
