#!/usr/bin/env python3
import json, datetime

with open('hammer_db.json') as f:
    h = json.load(f)

keys = list(h.keys())
print('Keys:', keys)
for k in keys:
    if isinstance(h[k], list):
        print(f'  {k}: {len(h[k])} items')
        if h[k]:
            print(f'    First item keys: {list(h[k][0].keys())[:8]}')
    elif isinstance(h[k], dict):
        print(f'  {k}: {len(h[k])} sub-keys')
        first5 = list(h[k].keys())[:5]
        print(f'    First 5 keys: {first5}')
    else:
        print(f'  {k}: {type(h[k]).__name__} = {str(h[k])[:80]}')

if 'meta' in h:
    print(f'\nmeta:')
    for mk, mv in h['meta'].items():
        print(f'  {mk}: {mv}')
if 'meta' in h and isinstance(h['meta'], dict) and 'last_updated' in h['meta']:
    print(f'\nlast_updated in meta: {h["meta"]["last_updated"]}')
if 'last_updated' in h:
    print(f'\nlast_updated (top-level): {h["last_updated"]}')

# Check for the recent change - find anything that says 2026-06-22 or 2026-06-23
print('\n--- Checking for recent dates in string values ---')
recent_hits = []
def search_recent(obj, path=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            search_recent(v, f'{path}.{k}')
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            search_recent(v, f'{path}[{i}]')
    elif isinstance(obj, str) and ('2026-06-22' in obj or '2026-06-23' in obj):
        recent_hits.append(f'{path}: {obj[:120]}')
search_recent(h)
for hit in recent_hits[:10]:
    print(hit)

# Count total hammers
if 'hammers' in h:
    print(f'\nTotal hammers: {len(h["hammers"])}')
    # Show suppliers
    for i, ham in enumerate(h['hammers']):
        name = ham.get('supplier', ham.get('name', '?'))
        print(f'  [{i+1}] {name}')
