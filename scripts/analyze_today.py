import json, datetime

now = datetime.datetime(2026, 6, 24, 23, 59, 59)
day_start = datetime.datetime(2026, 6, 24, 0, 0, 0)
epoch_start = int(day_start.timestamp())
epoch_end = int(now.timestamp())

print(f"Today epoch range: {epoch_start} - {epoch_end}")

incoming_today = []
outgoing_today = []

with open('C:\\nichenexusglobal\\whatsapp_messages.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        line=line.strip()
        if not line: continue
        try:
            m=json.loads(line)
            ts = m.get('data',{}).get('timestamp', m.get('timestamp', 0))
            if isinstance(ts, dict):
                ts_val = int(ts.get('low', 0))
            else:
                ts_val = int(ts) if ts else 0
            
            if epoch_start <= ts_val <= epoch_end:
                chat = m.get('data',{}).get('chat', m.get('chat','?'))
                is_from_me = m.get('data',{}).get('isFromMe', m.get('isFromMe', True))
                body = m.get('data',{}).get('body', m.get('body',''))[:120]
                t = datetime.datetime.fromtimestamp(ts_val)
                if is_from_me == False:
                    incoming_today.append((t, chat, body))
                else:
                    outgoing_today.append((t, chat, body))
        except Exception as e:
            pass

print(f"\nWA INCOMING TODAY: {len(incoming_today)}")
for t, chat, body in incoming_today:
    print(f"  {t} | {chat} | {body}")

print(f"\nWA OUTGOING TODAY: {len(outgoing_today)}")
for t, chat, body in outgoing_today:
    name = str(chat).split('@')[0] if '@' in str(chat) else chat
    print(f"  {t} | {name} | {body[:80]}")

# Also check send_log
print("\n--- SEND LOG CHECK ---")
with open('C:\\nichenexusglobal\\send_log.jsonl', 'r', encoding='utf-8') as f:
    slines = f.readlines()
print(f"Send log: {len(slines)} total records")

today_sent = []
for line in slines:
    line=line.strip()
    if not line: continue
    try:
        r=json.loads(line)
        ts = r.get('timestamp','')
        if '2026-06-24' in str(ts):
            today_sent.append(r)
    except: pass

if today_sent:
    print(f"Today sends: {len(today_sent)}")
    for r in today_sent:
        print(f"  {r.get('timestamp','?')} | {r.get('company','?')} | {r.get('email','?')} | cat={r.get('category','?')} | score={r.get('gate_score','?')}")
else:
    print("No sends logged for 2026-06-24")
    print("Last 5 records:")
    for line in slines[-5:]:
        line=line.strip()
        if not line: continue
        try:
            r=json.loads(line)
            print(f"  {str(r.get('timestamp','?'))[:19]} | {r.get('company','?')} | {r.get('email','?')} | {r.get('category','?')}")
        except: pass
