"""Check bridge queue for pending messages"""
import urllib.request, json

url = "http://127.0.0.1:3000/messages"
req = urllib.request.Request(url)
resp = urllib.request.urlopen(req, timeout=10)
messages = json.loads(resp.read())

# Find incoming (not from us)
incoming = [m for m in messages if not m.get("data", {}).get("isFromMe", True)]
print(f"Bridge queue: {len(messages)} total, {len(incoming)} incoming")

for m in incoming:
    data = m.get("data", {})
    push = data.get("pushName", "?")
    chat = data.get("chat", "?")
    body = data.get("body", "") or ""
    print(f"\n💬 {push} ({chat})")
    print(f"   {body[:200]}")
