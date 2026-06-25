#!/usr/bin/env python3
"""Summarize bullets_db.json"""
import json
with open('C:/nichenexusglobal/bullets_db.json') as f:
    data = json.load(f)
print('Top-level keys:', list(data.keys()))
for k, v in data.items():
    if isinstance(v, list):
        print(f'  {k}: {len(v)} items')
        if len(v) > 0:
            print(f'  First item keys: {list(v[0].keys()) if isinstance(v[0], dict) else type(v[0])}')
    elif isinstance(v, dict):
        print(f'  {k}: {len(v)} sub-keys')
    else:
        print(f'  {k}: {v}')
