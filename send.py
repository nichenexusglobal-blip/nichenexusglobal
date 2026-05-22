import smtplib, ssl, sys
from email.mime.text import MIMEText

EMAIL = "pen@nichenexusglobal.com"
PASSWORD = "4cd7vQ4GV59ATxxt"
TO = sys.argv[1]
SUBJECT = sys.argv[2]
BODY = sys.argv[3]

msg = MIMEText(BODY, "plain", "utf-8")
msg["From"] = f"nichenexusglobal <{EMAIL}>"
msg["To"] = TO
msg["Subject"] = SUBJECT

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.exmail.qq.com", 465, context=context) as server:
    server.ehlo()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, [TO], msg.as_string())
print("SENT")
