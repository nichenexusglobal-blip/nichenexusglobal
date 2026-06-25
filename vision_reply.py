"""Vision Africa: draft → review → send"""
import sys
sys.path.insert(0, "C:/nichenexusglobal")
from bullet_review import review_bullet

# His latest message
his_message = "More than sending the spec sheet is reconciling the price. I'd prefer dealing directly with manufacturers to access the best minimum price. Thanks"

our_reply = """Hi Paul, fair point. Let me address that directly.

We're a China-based sourcing company — not adding a margin. We work with multiple LiFePO4 factories and help you compare. You see real factory pricing, and payment goes direct to the factory.

On price: the $165 was for 1-10 units. At 50 units the same model drops to $145 EXW. And at 100+ we push even lower from our partner factories.

Would a comparison table across 3 models with factory pricing help you decide?

Best regards,
Pen
Nichenexusglobal"""

ok, score, checks = review_bullet("Vision Africa", "Nigeria", our_reply, is_reply=True, last_client_msg=his_message)
print(f"\n{'='*50}")
print(f"结果: {'PASS ✅' if ok else 'FAIL ❌'} -- Score: {score}/100")
for role, issues, max_pts in checks:
    pts = max_pts - 4 * len(issues)
    icon = "✅" if not issues else "⚠️"
    print(f"  {role}: {pts}/{max_pts} {icon}")
    for i in issues:
        print(f"    - {i}")

if ok:
    print("\n✅ 自检通过，开始发送...")
    import requests
    url = "http://127.0.0.1:3000/send"
    payload = {
        "chatId": "196795552559324@lid",
        "text": our_reply
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        result = r.json()
        if r.status_code == 200 and result.get("status") == "ok":
            print(f"✅ 已发送！ID: {result.get('id', 'unknown')}")
        else:
            print(f"❌ 发送失败: {result}")
    except Exception as e:
        print(f"❌ 网络错误: {e}")
else:
    print("\n❌ 自检未过，不发送")
