#!/usr/bin/env python3
"""Check WhatsApp messages JSONL with better error handling"""
import json

real_msgs = []
error_count = 0
with open('C:/nichenexusglobal/whatsapp_messages.jsonl', 'r', encoding='utf-8') as f:
    for line_num, line in enumerate(f, 1):
        line = line.strip()
        if not line: continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            error_count += 1
            if error_count <= 3:
                print(f'  JSON error at line {line_num}: {line[:80]}')
            continue
        
        event = d.get('event', '')
        data = d.get('data', {})
        isFromMe = data.get('isFromMe', True) if isinstance(data, dict) else True
        chat = d.get('chat', '') or (data.get('remoteJid', '') if isinstance(data, dict) else '')
        
        if event != 'message': continue
        if isFromMe: continue
        if '81609428590707@lid' in str(chat): continue
        
        real_msgs.append(d)

print(f'Total incoming non-system messages: {len(real_msgs)}')
print(f'JSON parse errors skipped: {error_count}')

for m in real_msgs[-10:]:
    data = m.get('data', {})
    chat = m.get('chat', data.get('remoteJid', ''))
    body = data.get('body', '')[:100] if isinstance(data, dict) else ''
    ts = m.get('timestamp', data.get('messageTimestamp', ''))
    print(f'  Chat:{chat} | Body:{body[:60]} | Ts:{ts}')
