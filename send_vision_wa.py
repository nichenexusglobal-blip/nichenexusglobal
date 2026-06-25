"""Send Vision Africa reply — direct via bridge"""
import json, urllib.request

chat_id = "196795552559324@lid"
message = """Hi, I hear you. You want the best price, not just information.

I'm a China-based sourcing partner working with verified LiFePO4 factories. Here are two options from one of our partner factories:

1. 1004Wh/500W (Pro) — $165 EXW  
2. 1004Wh/300W — $145 EXW  

Both LiFePO4, UK plug. What volume are you looking at for TO-GO? Higher quantities bring the price down significantly, and I will check across multiple factories to get you the best option.

Best regards,
Pen
Nichenexusglobal"""

# Try bridge /send endpoint
data = json.dumps({"chatId": chat_id, "text": message}).encode()
req = urllib.request.Request(
    "http://127.0.0.1:3000/send",
    data=data,
    headers={"Content-Type": "application/json"}
)
try:
    resp = urllib.request.urlopen(req, timeout=15)
    result = json.loads(resp.read())
    print(f"Bridge /send: {resp.status} — {json.dumps(result, ensure_ascii=False)[:200]}")
except Exception as e:
    print(f"Bridge /send failed: {e}")
    
    # Fallback: try wago-api
    print("\nTrying wago-api...")
    data2 = json.dumps({"chatId": chat_id, "text": message}).encode()
    req2 = urllib.request.Request(
        "http://127.0.0.1:3003/client/sendMessage/8619855653280",
        data=data2,
        headers={"Content-Type": "application/json"}
    )
    try:
        resp2 = urllib.request.urlopen(req2, timeout=15)
        result2 = json.loads(resp2.read())
        print(f"Wago-api: {resp2.status} — {json.dumps(result2, ensure_ascii=False)[:200]}")
    except Exception as e2:
        print(f"Wago-api failed: {e2}")
