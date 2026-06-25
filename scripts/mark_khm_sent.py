#!/usr/bin/env python
"""Mark KHM Megatools as sent in bullets_db.json"""
import json

path = r'C:\nichenexusglobal\bullets_db.json'
with open(path, 'r', encoding='utf-8') as f:
    db = json.load(f)

updated = False
for b in db['email_bullets']:
    if b.get('company') == 'KHM Megatools Corp.':
        b['sent'] = True
        b['sent_date'] = '2026-06-25'
        b['sent_channel'] = 'email'
        b['status'] = 'sent'
        # Store the actual email sent
        b['draft_email_sent'] = """Hi KHM team,

I was looking at your power station range at khmtools.com.ph and noticed you carry Yamato, Greenfield, Daiden and Wadfow models from 200W to 800W.

We're a sourcing company based in Shenzhen, China, working with partner factories that produce LiFePO4 portable power stations. Your current lineup stops at 800W (Yamato YM63-800 at ₱19,500) and uses Li-Ion batteries in the Daiden series.

LiFePO4 offers significantly more cycle life and better thermal stability. For reference, our typical wholesale pricing:

- 1024Wh/1000W ~ $145 FOB
- 1280Wh/1200W ~ $205 FOB
- 2048Wh/2400W ~ $298 FOB

If you're interested in adding LiFePO4 models or higher-capacity units to your product range, I'd be happy to send spec sheets and a formal quotation.

Best regards,
Pen"""
        updated = True
        break

if updated:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    print("SUCCESS: KHM Megatools marked as sent")
else:
    print("FAIL: Company not found")
