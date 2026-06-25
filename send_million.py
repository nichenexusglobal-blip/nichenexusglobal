#!/usr/bin/env python3
"""Send reply to M Million via WhatsApp"""
import urllib.request, json

chat_id = "2349164337200@s.whatsapp.net"
message = """Yes, we do. LiFePO4 (Lithium Iron Phosphate) — the safest lithium battery type for power stations.

We have a 1280Wh/1200W model at $205 FOB. UK plug, 220-240V, CE certified.

As for your questions:
- Price: $205 FOB (1280Wh model)
- Showroom: We work directly with factories, no retail showroom
- How to get it: You place an order, we handle production from our partner factory

Happy to send the spec sheet."""

data = json.dumps({"chatId": chat_id, "text": message}).encode()
req = urllib.request.Request(
    "http://127.0.0.1:3000/client/sendMessage/8619855653280",
    data=data,
    headers={"Content-Type": "application/json"}
)
try:
    resp = urllib.request.urlopen(req, timeout=10)
    result = json.loads(resp.read())
    msg_id = result.get("messageId", "?")
    print(f"✅ Sent to M Million | msgId: {msg_id}")
except Exception as e:
    print(f"❌ Failed: {e}")
