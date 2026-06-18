import os, json

f = r'C:/nichenexusglobal/whatsapp_messages.jsonl'
seen = r'C:/nichenexusglobal/wago-api/.last_wa_msg'

last = int(open(seen).read().strip()) if os.path.exists(seen) else 0

if not os.path.exists(f):
    print('No messages file')
    exit()

lines = open(f, encoding='utf-8').readlines()
count_new = len(lines) - last
new_msgs = []

print(f'Total lines in file: {len(lines)}')
print(f'Last processed index: {last}')
print(f'New lines since last check: {count_new}')

if count_new > 0:
    for line in lines[last:]:
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if d.get('event') == 'message' and not d.get('data', {}).get('isFromMe', True):
            new_msgs.append({
                'sender': d['data'].get('pushName', '?'),
                'body': d['data'].get('body', '')[:200],
                'timestamp': d.get('_received_at', '?')
            })

print(f'New incoming messages found: {len(new_msgs)}')
for i, msg in enumerate(new_msgs):
    print(f'  [{i+1}] from={msg["sender"]} at={msg["timestamp"]}: {msg["body"]}')
