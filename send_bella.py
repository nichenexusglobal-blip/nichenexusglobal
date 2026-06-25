"""Draft and send reply to Bella (SOUOP)"""
import sys
sys.path.insert(0, "C:/nichenexusglobal")
from bullet_review import review_bullet

reply = """Dear Bella,

Thank you for the detailed introduction and the catalog. It's great to connect with SOUOP.

Our current target African markets include Nigeria, Kenya, Tanzania, and the broader SADC region. Most of these markets use UK-style Type G plugs and 220-240V.

We're looking for portable power stations in the 1000Wh-2000Wh range, LiFePO4, with pure sine wave output, suitable for home backup and small business use. OEM/ODM capability is a plus as some of our clients want their own branding.

Could you recommend which of your models would best fit these markets and share FOB pricing?

Looking forward to your recommendation.

Best regards,
Pen
Nichenexusglobal"""

# Self-review (no client message since this is a follow-up to Bella's intro)
ok, score, checks = review_bullet("SOUOP/Pordie", "China", reply, channel="email", is_reply=True)

print(f"{'='*50}")
print(f"结果: {'PASS ✅' if ok else 'FAIL ❌'} -- Score: {score}/100")
for role, issues, max_pts in checks:
    pts = max_pts - 4 * len(issues)
    icon = "✅" if not issues else "⚠️"
    print(f"  {role}: {pts}/{max_pts} {icon}")
    for i in issues:
        print(f"    - {i}")

# If pass, send via SMTP
if ok:
    print("\n✅ 自检通过，准备发送...")
    import smtplib
    from email.mime.text import MIMEText
    
    pwd = None
    with open("C:/Users/leon/AppData/Local/hermes/profiles/nichenexusglobal/.env") as f:
        for line in f:
            if "EMAIL_PASSWORD" in line:
                pwd = line.split("=", 1)[1].strip()
                break
    
    msg = MIMEText(reply, "plain", "utf-8")
    msg["Subject"] = "Re: Fw: Fw: Inquiry: LiFePO4 portable power station catalog & pricing"
    msg["From"] = "pen@nichenexusglobal.com"
    msg["To"] = "bella@souoppowerstation.com"
    
    try:
        smtp = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465, timeout=15)
        smtp.login("pen@nichenexusglobal.com", pwd)
        smtp.send_message(msg)
        smtp.quit()
        print("✅ 已发送至 bella@souoppowerstation.com")
    except Exception as e:
        print(f"❌ 发送失败: {e}")
else:
    print("\n❌ 自检未过，不发送")
