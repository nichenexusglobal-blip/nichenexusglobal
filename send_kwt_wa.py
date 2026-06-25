"""Send KWT Tech Mart quote via WhatsApp"""
import sys
sys.path.insert(0, "C:/nichenexusglobal")
from bullet_review import review_bullet

chat_id = "256789633108@s.whatsapp.net"
message = """Hi KWT Tech Mart team, following up on our WhatsApp conversation — here's a product that could work for your Uganda market.

1280Wh LiFePO4 Portable Power Station, 1200W pure sine wave, UK plug (Type G), CE certified. $205 FOB Shenzhen, MOQ 10 units.

I can send product photos too. Would this be suitable for your customers?

Best regards,
Pen
Nichenexusglobal"""

# Self-review first
ok, score, checks = review_bullet("KWT Tech Mart", "Uganda", message, channel="whatsapp")
print(f"结果: {'PASS ✅' if ok else 'FAIL ❌'} -- Score: {score}/100")

if ok:
    import urllib.request, json
    data = json.dumps({"chatId": chat_id, "text": message}).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:3003/client/sendMessage/8619855653280",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req, timeout=15)
    result = json.loads(resp.read())
    print(f"✅ Sent! ID: {result.get('messageId', '?')}")
else:
    print("\n❌ Self-check failed, not sending")
