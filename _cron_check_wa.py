import json

with open('C:\\nichenexusglobal\\whatsapp_messages.jsonl', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if d.get('event') in ('message', 'message_create') and not d.get('data', {}).get('isFromMe', True):
            push_name = d['data'].get('pushName', '?')
            body = d['data'].get('body', '')[:60]
            sender = d['data'].get('sender', '?')
            print(f'LINE {i}: from={push_name} sender={sender} body={body}')
