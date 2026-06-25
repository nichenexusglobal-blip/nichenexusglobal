"""Vision Africa: revised draft → review → clean"""
import sys
sys.path.insert(0, "C:/nichenexusglobal")
from bullet_review import review_bullet

his_msg = "More than sending the spec sheet is reconciling the price. I'd prefer dealing directly with manufacturers to access the best minimum price. Thanks"

our_reply = """Hi Vision Africa team. Fair point — let me address that directly.

We're a China-based sourcing company. We work with multiple LiFePO4 factories and help you compare their pricing side by side. You see each factory's price and pay them directly. The margin is ours to cover our time — it's transparent, not hidden.

Two options for your TO-GO brand:

1. 1004Wh/500W (Pro): $165 EXW, 1-10 units
2. 1004Wh/300W: $145 EXW, 1-10 units

Both LiFePO4, Type G plug, CE certified. Higher volumes = better pricing.

I'll send a spec sheet with photos for both. Then you decide which fits your market.

Best regards,
Pen
Nichenexusglobal"""

ok, score, checks = review_bullet("Vision Africa", "Nigeria", our_reply, is_reply=True, last_client_msg=his_msg)

print(f"{'='*50}")
print(f"结果: {'PASS ✅' if ok else 'FAIL ❌'} -- Score: {score}/100")
for role, issues, max_pts in checks:
    pts = max_pts - 4 * len(issues)
    icon = "✅" if not issues else "⚠️"
    print(f"  {role}: {pts}/{max_pts} {icon}")
    for i in issues:
        print(f"    - {i}")
