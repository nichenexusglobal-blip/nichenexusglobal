#!/usr/bin/env python3
"""Analyze hammer_db.json: category counts and verification status"""
import json

with open('C:/nichenexusglobal/hammer_db.json','r') as f:
    db = json.load(f)

cats = db.get('categories', {})
print('=== Categories Summary ===')
for k, v in cats.items():
    hammers = v.get('hammers', [])
    verified = sum(1 for h in hammers if h.get('source', '').startswith('verified'))
    alibaba = sum(1 for h in hammers if h.get('source', '') == 'alibaba_listing')
    total = len(hammers)
    print(f'  {k}: {total} hammers ({verified} verified_email, {alibaba} alibaba_listing)')
    # Show top 3 verified hammers
    vh = [h for h in hammers if h.get('source', '').startswith('verified')]
    if vh:
        for h in vh[:3]:
            fob = h.get('fob_usd', {})
            fob_str = '; '.join([f'{k}=${v}' for k,v in fob.items()]) if fob else 'no FOB'
            print(f'    ✓ {h["name"]}: {fob_str}')

print(f'\nTotal hammers: {db["meta"]["total_hammers"]}')
print(f'Last updated: {db["meta"]["last_updated"]}')
print(f'Categories: {db["meta"]["categories"]}')
