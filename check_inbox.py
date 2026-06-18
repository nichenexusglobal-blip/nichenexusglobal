#!/usr/bin/env python3
import imaplib, ssl, re, base64, os, datetime

pw = os.environ.get("NICHE_EMAIL_PASSWORD", "")
if not pw:
    env_path = "/d/nichenexusglobal/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("NICHE_EMAIL_PASSWORD=***                    pw = line.split("=",1)[1].strip().strip("'\"")
                    break
if not pw:
    pw = base64.b64decode("NGNkN3ZRNEdWNTlBVHh4dA==").decode()

ctx = ssl.create_default_context()
imap = imaplib.IMAP4_SSL("imap.exmail.qq.com", 993, ssl_context=ctx)
imap.login("pen@nichenexusglobal.com", pw)
imap.select("INBOX")

status, ids = imap.search(None, "UNSEEN")
unseen = ids[0].split() if ids[0] else []
print("未读邮件:", len(unseen))

since = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%d-%b-%Y")
status, ids = imap.search(None, f"(SINCE {since})")
recent = ids[0].split() if ids[0] else []
print("近5天邮件:", len(recent))
print()

for i in recent[-15:]:
    s, data = imap.fetch(i, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
    if data and data[0] and data[0][1]:
        hdr = data[0][1]
        if isinstance(hdr, bytes):
            d = re.search(rb"^Date:\s*(.*)", hdr, re.M|re.I)
            f = re.search(rb"^From:\s*(.*)", hdr, re.M|re.I)
            ss = re.search(rb"^Subject:\s*(.*)", hdr, re.M|re.I)
            ds = d.group(1).decode("utf-8","replace")[:16] if d else "?"
            fs = f.group(1).decode("utf-8","replace")[:50] if f else "?"
            ss_str = ss.group(1).decode("utf-8","replace")[:60] if ss else "?"
            flag = " **UNREAD**" if i in unseen else ""
            print(f"  [{i}] {ds} | {fs} | {ss_str}{flag}")

imap.logout()
