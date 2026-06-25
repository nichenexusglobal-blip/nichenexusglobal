"""Test the new intent matching check against the Vision Africa case"""
import sys
sys.path.insert(0, "C:/nichenexusglobal")
from bullet_review import review_bullet

# Test Case 1: Our ACTUAL bad reply (the one that failed)
# Client said: "But you must have a strong financial base"
# We replied: "No inventory required" (wrong!)
print("=" * 60)
print("测试1: 客户问financial base → 我们回了不用备库存（答非所问）")
print("=" * 60)
client1 = "But you must have a strong financial base for us to work together"
reply1 = """Thank you for your reply. It's great to hear you own the TO-GO power station brand and are looking to expand in the Nigerian market.

We work on an order-based model: you place an order, we handle production and logistics from our partner factories in China. No upfront inventory required on your end.

A 1004Wh/500W LiFePO4 unit is $165 EXW. Would you like me to send the spec sheet and product photos?

Best regards,
Pen
Nichenexusglobal"""

ok, score, checks = review_bullet("Vision Africa", "Nigeria", reply1, is_reply=True, last_client_msg=client1)
print(f"\n结果: {'PASS ✅' if ok else 'NEEDS FIX ❌'} -- Score: {score}/100")
for role, issues, max_pts in checks:
    print(f"  {role}: {max_pts - 5*len(issues)}/{max_pts} {'✅' if not issues else '⚠️'}")
    for i in issues:
        print(f"    - {i}")

print()
print("=" * 60)
print("测试2: 改进版回复（同时回应financial base + 价格 + 中间商）")
print("=" * 60)

client2 = "More than sending the spec sheet is reconciling the price. I'd prefer dealing directly with manufacturers to access the best minimum price. Thanks"
reply2 = """Hello Paul,

I understand completely. You want the best factory price — I'd feel the same way.

We're not adding a markup. Our model is simple: we work with multiple LiFePO4 power station factories in China and help you compare across them. You see the prices from each factory and choose what fits your TO-GO brand best. Payment goes directly to the factory.

On pricing: The $165 EXW was for 1-10 units. At 50 units it drops to $145, and at 100+ units we can get even more competitive pricing from our partner factories.

Would you like me to prepare a comparison table across 3-4 different capacity points with factory pricing so you can see the options?

Best regards,
Pen
Nichenexusglobal"""

ok2, score2, checks2 = review_bullet("Vision Africa", "Nigeria", reply2, is_reply=True, last_client_msg=client2)
print(f"\n结果: {'PASS ✅' if ok2 else 'NEEDS FIX ❌'} -- Score: {score2}/100")
for role, issues, max_pts in checks2:
    print(f"  {role}: {max_pts - 5*len(issues)}/{max_pts} {'✅' if not issues else '⚠️'}")
    for i in issues:
        print(f"    - {i}")
