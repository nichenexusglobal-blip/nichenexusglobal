import json

# Compile full daily report
report_parts = []

report_parts.append("## 6月24日 每日复盘")
report_parts.append("")

# --- EMAIL CHECK RESULTS ---
report_parts.append("### 📤 今日发送")
# Bullets DB shows Genectra sent today
report_parts.append("- **Genectra (Chile)** — contacto@genectra.cl (email, gate_score=100)")
report_parts.append("- 其他渠道：send_log无6月24日记录")
report_parts.append("")

# Yesterday's context
report_parts.append("昨日(6月23日)延续发送（参考）：")
report_parts.append("- Get Off Grid Zambia (WhatsApp)")
report_parts.append("- Solar Mart Energi (WhatsApp)")
report_parts.append("- Pata Pawa (WhatsApp)")
report_parts.append("- KHM Megatools (email)")
report_parts.append("")

# --- INBOX ---
report_parts.append("### 📥 今日回信/新消息")
report_parts.append("")

# From email_check.py: supplier emails
report_parts.append("**收件箱（email_check.py快照）：**")
report_parts.append("- Pecron (Chris) — FOB报价+海运到肯尼亚/菲律宾跟进 (供应商)")
report_parts.append("- Bella (Souop Power) — LiFePO4便携站目录和报价 (供应商)")
report_parts.append("- IMAP currently blocked (Tencent rate limit), using cached snapshot")
report_parts.append("")

# WhatsApp unreads from email_check
report_parts.append("**WhatsApp待处理（email_check.py检测）：**")
report_parts.append("- Dong Solar Limited — 1条未读（自动回复）")
report_parts.append("- Macpower Solar — 2条未读（等待回复）")
report_parts.append("- M Millions — 4条未读（\"Do you have lithium batteries\"）")
report_parts.append("- bensolar56 — 1条未读（自动回复）")
report_parts.append("- Batteriq — 2条未读（等待回复）")
report_parts.append("")

# WA JSONL analysis
report_parts.append("**WhatsApp JSONL（今天0条新消息 — 最后活动6月23日）：**")
report_parts.append("- 无今日进出消息（JSONL记录到昨天23:47为止）")
report_parts.append("")

# Bullets analysis
report_parts.append("### 📊 子弹库状态")
report_parts.append("")
report_parts.append("**整体统计：**")
report_parts.append("| 指标 | 数值 |")
report_parts.append("|------|------|")
bullet_stats = []
with open('C:\\nichenexusglobal\\bullets_db.json','r') as f:
    db = json.load(f)
    eb = db.get('email_bullets', [])
    wb = db.get('whatsapp_bullets', [])
    total = len(eb) + len(wb)
    sent = len([b for b in eb+wb if b.get('status') in ['sent','replied'] or b.get('sent_date')])
    waiting = len([b for b in eb+wb if b.get('status') == 'sent' and not b.get('replied')])
    replied = len([b for b in eb+wb if b.get('replied') == True or b.get('status') == 'replied'])
    alive_email = len([b for b in eb if b.get('status') in ['researched','verified','gated'] and not b.get('sent_date')])
    alive_wa = len([b for b in wb if b.get('status') in ['researched','verified','gated'] and not b.get('sent_date')])
    
    report_parts.append(f"| 子弹总数 | {total} (email={len(eb)}, WA={len(wb)}) |")
    report_parts.append(f"| 累计已发 | {sent} |")
    report_parts.append(f"| 今日新增 | 1 (Genectra) |")
    report_parts.append(f"| 活弹（未发可发） | {alive_email+alive_wa} (email={alive_email}, WA={alive_wa}) |")
    report_parts.append(f"| 已发等回 | {waiting} |")
    report_parts.append(f"| 客户回复 | {replied} (Genectra + ?) |")

report_parts.append("")

# Tomorrow's plan
report_parts.append("### 🎯 明日计划建议")
report_parts.append("")
report_parts.append("1. **处理WhatsApp待回复** — M MILLIONS问锂电池，这是直接询盘，优先回复")
report_parts.append("2. **Macpower Solar + Batteriq** — 已有消息待处理，确认是否为询盘")
report_parts.append("3. **修复IMAP** — Tencent企业邮登录异常，需检查密码/频率限制")
report_parts.append("4. **Pecron报价跟进** — Chris发了两次FOB+运费的跟进，可更新锤子库")
report_parts.append("5. **继续外发** — 5颗活弹（邮箱）可继续发，Genectra的回复可跟进（他们让发info到contacto@genectra.cl）")

print('\n'.join(report_parts))
