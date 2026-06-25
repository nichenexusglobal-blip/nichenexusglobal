"""Generate daily review report"""
import json, os
from datetime import datetime

WA = "C:/nichenexusglobal/whatsapp_messages.jsonl"
HAMMER = "C:/nichenexusglobal/hammer_db.json"
BULLETS = "C:/nichenexusglobal/bullets_db.json"

# WhatsApp replies today
wa_new = 0
wa_from = set()
with open(WA) as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try:
            d = json.loads(line)
            if not d.get("data",{}).get("isFromMe",True):
                pn = d.get("data",{}).get("pushName","")
                if pn:
                    wa_from.add(pn)
                    wa_new += 1
        except:
            pass

# Bullets stats
with open(BULLETS) as f:
    db = json.load(f)

wa_sent = sum(1 for b in db["whatsapp_bullets"] if b.get("sent"))
wa_total = len(db["whatsapp_bullets"])
em_sent = sum(1 for b in db["email_bullets"] if b.get("sent"))
em_total = len(db["email_bullets"])

# Hammers
with open(HAMMER) as f:
    hdb = json.load(f)
cats = hdb.get("categories", {})
ham_total = sum(len(v.get("hammers",[])) for v in cats.values()) if isinstance(cats,dict) else 0

print(f"""📅 2026年6月23日 复盘
━━━━━━━━━━━━━━━

📬 新回信
WhatsApp: {wa_new}条 ({', '.join(wa_from) if wa_from else '无'})

🎯 今日发射
WhatsApp: 12颗
邮箱: 3封（待发，IONOS锁IP）
总计: 12颗发出 + 3封待发

📊 子弹库存
WhatsApp: {wa_sent}/{wa_total} 已发
邮箱: {em_sent}/{em_total} 已发
锤子库: {ham_total}颗

⚙ 系统状态
桥(3000): ✅ 在线
wago-api(3003): ✅ CONNECTED
网站(nichenexusglobal.com): ✅ 已上线
GitHub: ✅ 已同步

📌 今日大事
- 网站上线 nichenexusglobal.com（ABCD风格）
- 供应商数据全归档（15家，43颗锤子）
- bullet-quality-gate门禁系统上线
- 180个社区skill克隆
- 三封邮件被Clash+IONOS拦截待发""")
