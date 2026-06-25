import json
import subprocess

today_replies = []
with open('C:\\nichenexusglobal\\whatsapp_messages.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try:
            msg = json.loads(line)
            ts = str(msg.get('timestamp', ''))
            if '2026-06-24' in ts or ts.startswith('2026-06-24'):
                # isFromMe could be False, 'false', or not present (fromMe instead)
                is_from_me = msg.get('isFromMe', msg.get('fromMe', True))
                if is_from_me in [False, 'false'] or (isinstance(is_from_me, bool) and not is_from_me):
                    chat = msg.get('chat','') or msg.get('chatId','') or msg.get('jid','') or '?'
                    body = (msg.get('body','') or msg.get('message','') or msg.get('text','') or '')[:120]
                    today_replies.append((chat, body, ts))
        except:
            pass

if today_replies:
    print(f"WA_INCOMING_TODAY: {len(today_replies)}")
    for chat, body, ts in today_replies:
        name_part = chat.split('@')[0] if '@' in str(chat) else chat
        print(f"  {ts[:19]} | {name_part} | {body}")
else:
    print("WA_INCOMING_TODAY: 0")
    print("--- LAST 20 WA MESSAGES ---")
    result = subprocess.run(['tail', '-20', 'C:\\nichenexusglobal\\whatsapp_messages.jsonl'], capture_output=True, text=True, shell=True)
    for line in result.stdout.strip().split('\n'):
        line = line.strip()
        if not line: continue
        try:
            m = json.loads(line)
            ts = m.get('timestamp', '?')
            fromMe = m.get('isFromMe', m.get('fromMe', '?'))
            chat = m.get('chat', '') or m.get('chatId', '') or m.get('jid', '') or '?'
            body = (m.get('body', '') or m.get('message', '') or m.get('text', '') or '')[:80]
            print(f"  {str(ts)[:19]} | fromMe={fromMe} | {str(chat)[:30]} | {body}")
        except:
            pass
