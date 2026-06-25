"""Find unsent bullets - both WhatsApp and Email"""
import json

with open("C:/nichenexusglobal/bullets_db.json", "r") as f:
    db = json.load(f)

print("=== UNSENT WHATSAPP BULLETS ===")
wa_unsent = [b for b in db.get("whatsapp_bullets", []) if not b.get("sent")]
for b in wa_unsent:
    print(f"\n🔴 {b['company']} ({b['market']})")
    print(f"   Segment: {b.get('segment','?')}")
    print(f"   WhatsApp: {b.get('whatsapp','?')}")
    print(f"   Status: {b.get('status','?')}")
    print(f"   Draft: {str(b.get('draft',''))[:200]}")

print(f"\n\nTotal unsent WA: {len(wa_unsent)}")

print("\n\n=== UNSENT EMAIL BULLETS ===")
em_unsent = [b for b in db.get("email_bullets", []) if not b.get("sent")]
for b in em_unsent[:10]:  # First 10
    print(f"\n📧 {b['company']} ({b['market']})")
    print(f"   Email: {b.get('email','?')}")
    print(f"   Segment: {b.get('segment','?')}")
    print(f"   Draft: {str(b.get('draft',''))[:200]}")

print(f"\n\nTotal unsent email: {len(em_unsent)}")
print(f"\nShowing first 10 of {len(em_unsent)}")
