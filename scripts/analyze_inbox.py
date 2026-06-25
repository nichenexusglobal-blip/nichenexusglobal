#!/usr/bin/env python3
"""Read the saved inbox data and analyze it"""
import json

INPUT = '/c/nichenexusglobal/inbox_data.jsonl'

suppliers = {}
keys_of_interest = ['fob','exw','moq','price','shipping','delivery','lead time',
                    'oem','cert','payment','sample','order','catalog','quote']

try:
    with open(INPUT, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line)
            from_addr = entry.get('from', '')
            subj = entry.get('subject', '')
            body = entry.get('body', '')
            date = entry.get('date', '')
            
            # Extract supplier name from email
            name = from_addr.split('@')[0].lower()
            name = name.strip('"').strip("'")
            
            # Skip obvious non-supplier
            if not name or name in ['info', 'sales', 'contact', 'support']:
                # Try domain
                dom_match = __import__('re').search(r'@([\w-]+\.\w+)', from_addr)
                if dom_match:
                    name = dom_match.group(1)
            
            if name not in suppliers:
                suppliers[name] = {
                    'from': from_addr,
                    'emails': []
                }
            
            # Extract key info
            info = {}
            body_lower = body.lower()
            
            # Price extraction
            prices = __import__('re').findall(r'\$\s*\d+\.?\d*', body)
            if prices:
                info['prices_mentioned'] = prices[:5]
            
            # MOQ
            moq = __import__('re').search(r'moq[:\s]*(\d+)', body_lower)
            if moq:
                info['moq'] = moq.group(1)
            
            # FOB
            has_fob = 'fob' in body_lower
            has_exw = 'exw' in body_lower
            
            # Shipping
            ship_kws = ['shipping','delivery','freight','cbm','container']
            has_ship = any(k in body_lower for k in ship_kws)
            
            if has_fob or has_exw or has_ship or prices:
                info['has_fob'] = has_fob
                info['has_exw'] = has_exw
                info['has_shipping'] = has_ship
            
            suppliers[name]['emails'].append({
                'date': date,
                'subject': subj[:100],
                'info': info,
                'body_preview': body[:300]
            })
    
    print(f"=== SUPPLIER EMAILS FOUND: {len(suppliers)} ===\n")
    
    for name, data in sorted(suppliers.items(), key=lambda x: len(x[1]['emails']), reverse=True):
        print(f"\n{'='*50}")
        print(f"📧 {name} ({data['from'][:60]}) — {len(data['emails'])} emails")
        print('='*50)
        
        for em in data['emails']:
            info = em['info']
            prefix = ''
            if info.get('has_fob'): prefix += '💰'
            if info.get('has_shipping'): prefix += '🚢'
            if info.get('prices_mentioned'): prefix += '💲'
            
            print(f"\n  {em['date']} {prefix}")
            print(f"  Subj: {em['subject']}")
            if info.get('moq'): print(f"  MOQ: {info['moq']}")
            if info.get('prices_mentioned'): print(f"  Prices: {', '.join(info['prices_mentioned'])}")
            
            # Print body
            body = em['body_preview']
            if body:
                print(f"  Body:\n{body}\n")

except FileNotFoundError:
    print(f"File {INPUT} not found - run full_inbox_scan.py first")
except Exception as e:
    print(f"ERROR: {e}")
