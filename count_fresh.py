#!/usr/bin/env python3
import json

db = json.load(open('bullets_db.json'))
wa = db['whatsapp_bullets']

# True unsent: status = verified AND no sent field or sent = false
# AND must be newly added (after the last cleanup)
really_unsent = []
for b in wa:
    is_unsent = b.get('status') in ('verified',) and (b.get('sent') != True)
    # Also check: no sent_channel or sent_date fields
    has_no_sent_evidence = not b.get('sent_channel') and not b.get('sent_date') and not b.get('last_sent')
    # And check sent flag explicitly
    sent_explicitly = b.get('sent') == True
    
    if is_unsent and not sent_explicitly:
        really_unsent.append(b)

print(f"Truly unsent WhatsApp bullets: {len(really_unsent)}")
for i, b in enumerate(really_unsent):
    print(f"  {i+1}. {b['company']} ({b['market']}) WA:{b.get('whatsapp','?')}")
