#!/usr/bin/env python3
"""Check incoming WhatsApp messages - show recent non-auto-reply ones"""
import json

real_msgs = []
with open('C:/nichenexusglobal/whatsapp_messages.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try:
            d = json.loads(line)
        except:
            continue
        
        event = d.get('event', '')
        data = d.get('data', {})
        isFromMe = data.get('isFromMe', True) if isinstance(data, dict) else True
        chat = data.get('chat', '') if isinstance(data, dict) else ''
        body = data.get('body', '') if isinstance(data, dict) else ''
        
        if event != 'message': continue
        if isFromMe: continue
        if '81609428590707@lid' in str(chat): continue
        
        real_msgs.append(d)

print(f'Total incoming non-system: {len(real_msgs)}')

# Show last 20 non-auto-reply
auto_keywords = ['thank you for contacting', 'thank you for reaching', 'we are currently closed',
                 'one of our team members', 'please let us know how we can help']
non_auto = [m for m in real_msgs if not any(k in (m.get('data',{}).get('body','')).lower() for k in auto_keywords)]

print(f'Non-auto-reply: {len(non_auto)}')
for m in non_auto[-20:]:
    data = m.get('data', {})
    body = data.get('body', '')[:120] if isinstance(data, dict) else ''
    push = data.get('pushName', '') if isinstance(data, dict) else ''
    ts = data.get('timestamp', m.get('timestamp', '')) if isinstance(data, dict) else ''
    print(f'  {push}: {body}')
