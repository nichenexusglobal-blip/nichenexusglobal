"""Vision Africa: v4 with fixes"""
import sys
sys.path.insert(0, "C:/nichenexusglobal")
from bullet_review import review_bullet

his_msg = "More than sending the spec sheet is reconciling the price. I'd prefer dealing directly with manufacturers to access the best minimum price. Thanks"

our_reply = """Hi, I hear you. You want the best price, not just information.

I'm a China-based sourcing partner working with verified LiFePO4 factories. Here are two options from one of our partner factories:

1. 1004Wh/500W (Pro) — $165 EXW  
2. 1004Wh/300W — $145 EXW  

Both LiFePO4, UK plug. What volume are you looking at for TO-GO? Higher quantities bring the price down significantly, and I will check across multiple factories to get you the best option.

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
