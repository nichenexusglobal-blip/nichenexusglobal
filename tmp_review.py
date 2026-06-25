import json

db = json.load(open('C:/nichenexusglobal/bullets_db.json'))

# Today's new sends (2026-06-24)
today_sent_email = [b for b in db.get('email_bullets',[]) if b.get('sent_date')=='2026-06-24']
today_sent_wa = [b for b in db.get('whatsapp_bullets',[]) if b.get('sent_date')=='2026-06-24']

print("=== EMAIL sent today (2026-06-24) ===")
for b in today_sent_email:
    print(f'{b["company"]} | {b["market"]} | {b.get("sent_channel","email")} | status={b["status"]}')
print()

print("=== WHATSAPP sent today (2026-06-24) ===")
for b in today_sent_wa:
    print(f'{b["company"]} | {b["market"]} | {b.get("sent_channel","whatsapp")} | status={b["status"]} | last_reply={b.get("last_reply","-")}')
print()

# All bullets stats
all_email = db.get("email_bullets",[])
all_wa = db.get("whatsapp_bullets",[])
all_bullets = all_email + all_wa

sent = [b for b in all_bullets if b.get("sent")==True and b.get("status") not in ["closed_no_followup"] and "no_match" not in b.get("sent_note","") and "no_contact" not in b.get("sent_note","")]
replied = [b for b in all_bullets if b.get("status","").startswith("replied")]
alive = [b for b in all_bullets if b.get("sent")==False and b.get("status") not in ["closed_no_followup","no_contact_found"] and b.get("gate_score",0)>=75 and b.get("email","")+b.get("whatsapp","")!=""]

print(f"Total email bullets: {len(all_email)}")
print(f"Total WA bullets: {len(all_wa)}")
print(f"Sent (active): {len(sent)}")
print(f"Replied: {len(replied)}")
print(f"Alive unsent: {len(alive)}")
print()
print("=== REPLIED bullets ===")
for b in replied:
    print(f'  {b["company"]} ({b["market"]}) | last_reply: {b.get("last_reply","-")[:100]}')
