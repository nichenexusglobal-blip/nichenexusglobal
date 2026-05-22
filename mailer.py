"""
nichenexusglobal — 腾讯企业邮箱邮件发送模块
使用 SMTP SSL 直接发送邮件
"""

import smtplib
import ssl
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = "smtp.exmail.qq.com"
SMTP_PORT = 465

EMAIL_ADDRESS = "pen@nichenexusglobal.com"
EMAIL_PASSWORD = "4cd7vQ4GV59ATxxt"


def send_email(to: str, subject: str, body: str, cc: str = None, reply_to: str = None) -> dict:
    """发送一封邮件"""
    msg = MIMEMultipart('alternative')
    msg["From"] = f"nichenexusglobal <{EMAIL_ADDRESS}>"
    msg["To"] = to
    msg["Subject"] = subject
    
    if cc:
        msg["Cc"] = cc
    if reply_to:
        msg["Reply-To"] = reply_to
    
    msg.attach(MIMEText(body, "plain", "utf-8"))
    html = body.replace("\n", "<br>\n")
    msg.attach(MIMEText(f"<html><body>{html}</body></html>", "html", "utf-8"))
    
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
            server.ehlo()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            
            recipients = [to]
            if cc:
                recipients.append(cc)
            
            server.sendmail(EMAIL_ADDRESS, recipients, msg.as_string())
            
        return {"status": "sent", "to": to, "subject": subject}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def test_connection() -> dict:
    """测试 SMTP 连接"""
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
            server.ehlo()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        return {"status": "ok", "message": "SMTP connection successful"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    result = test_connection()
    print(json.dumps(result, ensure_ascii=False, indent=2))
