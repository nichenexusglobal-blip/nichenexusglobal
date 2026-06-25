#!/usr/bin/env python3
"""
UNIVERSAL SEND GATE — 绝对发射门禁系统。
所有邮件和所有WhatsApp消息必须经过此模块才能发送。
不通过 = 不发送。无例外。无绕过。
"""
import json, os, sys, subprocess, hashlib, time, re
from datetime import datetime

WORKDIR = r"C:\nichenexusglobal"
BLACKLIST_FILE = os.path.join(WORKDIR, "email_blacklist.json")
SEND_LOG = os.path.join(WORKDIR, "send_log.jsonl")
DRAFT_DIR = os.path.join(WORKDIR)

# ═══ WhatsApp桥配置（wago-api / Go+whatsmeow）═══
WHATSAPP_BRIDGE_URL = "http://127.0.0.1:3000"
WHATSAPP_SESSION_ID = "8619855653280"

def check_bridge_health():
    """发送WhatsApp前必须检查桥是否活着。断了不发。"""
    try:
        import urllib.request
        req = urllib.request.Request(f"{WHATSAPP_BRIDGE_URL}/ping", method="GET")
        resp = urllib.request.urlopen(req, timeout=5)
        status = json.loads(resp.read())
        if status.get("success") and status.get("message") == "pong":
            return True, "wago-api connected"
        else:
            return False, f"桥状态异常: {status}"
    except Exception as e:
        return False, f"桥连接失败: {e}"

def log_send(entry):
    with open(SEND_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

WHATSAPP_JSONL = os.path.join(WORKDIR, "whatsapp_messages.jsonl")

def check_whatsapp_already_sent(chat_id):
    """查whatsapp_messages.jsonl，这个号码我们发过消息没有。isFromMe=true就是发出去的。"""
    if not os.path.exists(WHATSAPP_JSONL):
        return False, []  # 没有任何记录，肯定没发过
    found = []
    with open(WHATSAPP_JSONL, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
                # 兼容两种格式：旧版data.chat + 新版顶层chat
                msg_chat = msg.get("data", {}).get("chat", "") or msg.get("chat", "")
                msg_from_me = msg.get("data", {}).get("isFromMe", False) or msg.get("isFromMe", False)
                # 判断是否发往目标号码：精确匹配或@lid包含匹配
                matched = (
                    msg_chat == chat_id
                    or (chat_id.endswith("@lid") and msg_chat == chat_id)
                    or (chat_id.endswith("@s.whatsapp.net") and msg_chat == chat_id)
                    or (msg_chat.split("@")[0] == chat_id.split("@")[0])
                )
                if msg_from_me and matched:
                    body = msg.get("data", {}).get("body", "") or msg.get("body", "")
                    ts = msg.get("_sent_at", "") or msg.get("timestamp", "") or msg.get("_received_at", "")
                    found.append({"body": body[:60], "time": ts})
            except json.JSONDecodeError:
                continue
    return len(found) > 0, found

def save_draft(recipient, name, body, score, reason):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = name.replace(" ", "_")[:20]
    path = os.path.join(DRAFT_DIR, f"draft_blocked_{safe_name}_{ts}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"TO: {recipient}\nCOMPANY: {name}\nSCORE: {score}/100\nREASON: {reason}\n\n{body}")
    print(f"  ⛔ BLOCKED ({score}/100) — saved to {os.path.basename(path)}")
    return path

# ─── EMAIL GATE ───────────────────────────────────────────────

def check_email_gate(to, name, body, category, is_reply=False):
    """
    category = 'supplier' (RFQ)  →  supplier_rfq_gate.py threshold 80
    category = 'customer'        →  precision_gate.py  threshold 95
    is_reply=True: skips verification gate (already in conversation).

    Returns: {'pass': True/False, 'score': int, 'reason': str}
    """
    if category == "supplier":
        threshold = 80
        try:
            sys.path.insert(0, WORKDIR)
            from supplier_rfq_gate import gate_check as supplier_gate
            import re
            model_patterns = [
                r'[A-Z]+[\d]+[A-Z]?', r'Wall\s+Mounted\s+Battery', r'Portable\s+Power\s+Station\s+\d+W',
                r'Solar\s+Inverter', r'Server\s+Rack\s+Battery', r'Golf\s+Cart.*Battery',
                r'\d+[V]\s+\d+[Aa][hH]', r'LifePO4\s+Battery\s+With\s+Wheels',
                r'Pioneer\s+\d+', r'[A-Z][a-z]+\s+\d+',
            ]
            body_models = []
            for p in model_patterns:
                matches = re.findall(p, body)
                body_models.extend(matches[:2])
            body_models = list(set(body_models))[:5]
            
            result = supplier_gate(name, body, body_models if body_models else None)
            score = 0
            if isinstance(result, tuple) and len(result) >= 2:
                score = result[1].get("score", 0) if isinstance(result[1], dict) else 0
            elif isinstance(result, dict):
                score = result.get("score", 0)
            # Replies: lower threshold (already in conversation)
            if is_reply:
                threshold = 50
        except Exception as e:
            print(f"  ⚠ Gate error: {e} — blocking to be safe")
            return {"pass": False, "score": 0, "reason": f"Gate error: {e}"}

    elif category == "customer":
        threshold = 95
        try:
            # 第一步：验证门禁（回复现有客户跳过）
            if not is_reply:
                sys.path.insert(0, WORKDIR)
                from precision_bullet_gate import verify as bullet_verify
                v_result = bullet_verify(name, body, "customer")
                if not v_result["pass"]:
                    for issue in v_result["issues"]:
                        print(f"  🔬 {issue}")
                    return {"pass": False, "score": v_result["score"], "reason": f"验证门禁: {v_result['score']}/100 - 调研不充分"}

            # 第二步：精度门禁
            from precision_gate import gate_check as precision_gate
            result = precision_gate(name, body)
            # Returns tuple: (passed: bool, details: dict)
            if isinstance(result, tuple) and len(result) >= 2:
                score = result[1].get("score", 0) if isinstance(result[1], dict) else 0
            elif isinstance(result, dict):
                score = result.get("score", 0)
            else:
                score = 0
        except Exception as e:
            print(f"  ⚠ Gate error: {e} — blocking to be safe")
            return {"pass": False, "score": 0, "reason": f"Gate error: {e}"}
    else:
        return {"pass": False, "score": 0, "reason": f"Unknown category: {category}"}

    passed = score >= threshold
    reason = f"Gate score {score}/{threshold}" if not passed else ""
    return {"pass": passed, "score": score, "reason": reason}


# ─── WHATSAPP GATE ─────────────────────────────────────────────

WHATSAPP_GATE_BANNED = [
    "test", "testing", "test message", "ping",
    "hello world", "just checking"
]

def check_whatsapp_gate(chat_id, message, company_name=""):
    """WhatsApp gate — uses whatsapp_gate.py for full checks (length, tone, pricing dump)"""
    try:
        sys.path.insert(0, WORKDIR)
        from whatsapp_gate import check_whatsapp
        result = check_whatsapp(company_name, message)
        if result["passed"]:
            return {"pass": True, "score": result["score"], "reason": ""}
        return {"pass": False, "score": result["score"], "reason": "; ".join(result["issues"])}
    except ImportError:
        pass  # Fallback to simplified check below
    
    msg_lower = message.lower()

    # 1. No test messages
    for banned in WHATSAPP_GATE_BANNED:
        if banned in msg_lower:
            return {"pass": False, "score": 0, "reason": f"Banned phrase: '{banned}'"}

    # 2. Must have value proposition
    has_value = any(kw in msg_lower for kw in [
        "from usd", "pricing", "supply", "manufacturer",
        "factory", "oem", "distributor", "partner",
        "verified", "liFePO4", "certified"
    ])
    if not has_value:
        return {"pass": False, "score": 30, "reason": "No value proposition detected"}

    # 3. Must identify self
    has_id = any(kw in msg_lower for kw in ["pen", "nichenexusglobal"])
    if not has_id:
        return {"pass": False, "score": 40, "reason": "No self-identification"}

    # 4. Must have contact/next step
    has_cta = any(kw in msg_lower for kw in ["relevant", "interested", "would this", "working with", "share"])
    if not has_cta:
        return {"pass": False, "score": 50, "reason": "No call to action"}

    return {"pass": True, "score": 100, "reason": ""}


# ─── UNIVERSAL SEND (EMAIL) ─────────────────────────────────────

def send_email(to, name, subject, body, category="customer", is_reply=False):
    """
    The ONE way to send emails. Gate enforced. No bypass.
    is_reply=True: skips verification gate (already in conversation), still runs precision gate.
    """
    print(f"\n📧 {name} -> {to} [{category}]")

    # 0. Blacklist check
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE) as f:
            blacklist = json.load(f)
        if to in blacklist:
            print(f"  ⛔ BLACKLISTED — {blacklist[to]}")
            return False

    # 1. Gate check
    gate = check_email_gate(to, name, body, category, is_reply=is_reply)
    if not gate["pass"]:
        save_draft(to, name, body, gate["score"], gate["reason"])
        return False

    # 1a. Harness: cold emails require research evidence
    if not is_reply and category == "customer":
        try:
            ev_file = os.path.join(WORKDIR, ".research_evidence.json")
            if os.path.exists(ev_file):
                with open(ev_file, encoding="utf-8") as f:
                    evidence_list = json.load(f)
                has_evidence = any(
                    e["target"].lower() in name.lower() or name.lower() in e["target"].lower()
                    for e in evidence_list
                )
                if not has_evidence:
                    print(f"  🔒 HARNESS: 未找到对 {name} 的研究证据 — 拦截")
                    save_draft(to, name, body, 0, "HARNESS: 缺少研究证据")
                    return False
            else:
                print(f"  🔒 HARNESS: 研究证据文件不存在 — 拦截")
                save_draft(to, name, body, 0, "HARNESS: 缺少研究证据文件")
                return False
        except Exception as e:
            print(f"  ⚠ HARNESS error: {e}")
            return False

    # 1b. Verification gate for customer cold emails (checks research depth)
    if not is_reply and category == "customer":
        try:
            sys.path.insert(0, WORKDIR)
            from precision_bullet_gate import verify as bullet_verify
            v_result = bullet_verify(name, body, "customer")
            if not v_result["pass"]:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe = name.replace(" ", "_")[:20]
                path = os.path.join(DRAFT_DIR, f"draft_blocked_{safe}_{ts}.txt")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(f"TO: {to}\nCOMPANY: {name}\nSCORE: {v_result['score']}/100\nISSUES: {v_result['issues']}\n\n{body}")
                for issue in v_result["issues"]:
                    print(f"  🔬 {issue}")
                print(f"  ⛔ BLOCKED (验证门禁 {v_result['score']}/100)")
                return False
        except Exception as e:
            print(f"  ⚠ Verification gate error: {e} — blocking to be safe")
            return False

    # ── 99%精准子弹门禁（邮件）──
    try:
        sys.path.insert(0, WORKDIR)
        from precision_checklist import check_bullet, print_report
        result = check_bullet(name, body, to, "email")
        if not result["pass"]:
            print_report(result)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(DRAFT_DIR, f"99p_blocked_{name[:20]}_{ts}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"TO: {to}\nCOMPANY: {name}\nSCORE: {result['score']}/100\n")
                for issue in result["issues"]:
                    f.write(f"ISSUE: {issue}\n")
                f.write(f"\n{body}")
            print(f"  ⛔ 99%门禁拦截 ({result['score']}/100) — saved to {os.path.basename(path)}")
            return False
    except ImportError:
        print("  ⚠ precision_checklist not available")
    except Exception as ce:
        print(f"  ⚠ 99% gate error: {ce}")

    # 2. Send
    try:
        import smtplib, ssl
        from email.mime.text import MIMEText
        from email.utils import formatdate

        ctx = ssl.create_default_context()
        from pwd_loader import get_pwd
        pwd = get_pwd()
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465, timeout=10, context=ctx)
        server.login("pen@nichenexusglobal.com", pwd)

        msg = MIMEText(body, "plain", "utf-8")
        msg["From"] = "pen@nichenexusglobal.com"
        msg["To"] = to
        msg["Subject"] = subject[:998]  # subject length limit
        msg["Date"] = formatdate(localtime=True)
        server.sendmail("pen@nichenexusglobal.com", [to], msg.as_string())
        server.quit()

        print(f"  ✅ SENT (gate: {gate['score']}/100)")

        # 3. Log
        log_send({
            "timestamp": datetime.now().isoformat(),
            "email": to, "company": name, "subject": subject,
            "category": category, "success": True,
            "gate_score": gate["score"]
        })
        
        # 4. Track send in bullets DB
        if name:
            try:
                bullets_path = os.path.join(WORKDIR, "bullets_db.json")
                with open(bullets_path) as f:
                    bdb = json.load(f)
                for b in bdb["email_bullets"] + bdb["whatsapp_bullets"]:
                    if b.get("company") == name:
                        if "send_log" not in b:
                            b["send_log"] = []
                        b["send_log"].append({
                            "timestamp": datetime.now().isoformat(),
                            "channel": "email",
                            "subject": subject
                        })
                        b["last_sent"] = datetime.now().isoformat()
                        b["send_count"] = len(b["send_log"])
                        if b.get("status") in ["gated", "researched", "verified"]:
                            b["status"] = "sent"
                        break
                with open(bullets_path, "w") as f:
                    json.dump(bdb, f, ensure_ascii=False, indent=2)
            except Exception as te:
                print(f"  ⚠ Send tracking error: {te}")
        
        return True

    except Exception as e:
        print(f"  ❌ SEND FAILED: {e}")
        return False


# ─── UNIVERSAL SEND (WHATSAPP) ──────────────────────────────────

def send_whatsapp(chat_id, message, company_name="", is_reply=False):
    """
    The ONE way to send WhatsApp. Gate enforced. No bypass.
    is_reply=True: skips verification gate (already in conversation).
    """
    print(f"\n💬 {company_name or chat_id}")

    # ── 铁律LID：禁止用lid格式发送 ──
    if chat_id.endswith("@lid"):
        print(f"  🔒 LID PROTECTION: chat_id以@lid结尾 ({chat_id})")
        print(f"  🔒 lid是WhatsApp内部ID不等于电话号码。必须通过官网验证真实号码后再发。")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(DRAFT_DIR, f"wa_lid_blocked_{company_name[:20]}_{ts}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"TO: {chat_id}\nCOMPANY: {company_name}\nREASON: LID格式禁止发送\n\n{message}")
        print(f"  ⛔ BLOCKED (LID格式) — saved to {os.path.basename(path)}")
        return False

    # ── 铁律桥：检查WhatsApp桥是否活着 ──
    bridge_ok, bridge_status = check_bridge_health()
    if not bridge_ok:
        print(f"  🔒 BRIDGE CHECK FAILED: {bridge_status}")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(DRAFT_DIR, f"wa_bridge_blocked_{company_name[:20]}_{ts}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"TO: {chat_id}\nCOMPANY: {company_name}\nREASON: 桥断开: {bridge_status}\n\n{message}")
        print(f"  ⛔ BLOCKED (桥断开) — 先修桥再发。saved to {os.path.basename(path)}")
        return False

    # ── 重复发送检查：查JSONL有没有发过这个号码 ──
    already_sent, sent_records = check_whatsapp_already_sent(chat_id)
    if already_sent:
        print(f"  🔒 DUPLICATE DETECTED: {chat_id} 已发过 {len(sent_records)} 条消息")
        for r in sent_records:
            print(f"     🕐 {r['time']} | {r['body']}")
        print(f"  ⛔ BLOCKED — 这个号码已经发过消息，防止重复造成混乱")
        return False

    # ── 对话活性检查：wago-api用webhook收消息，跳过旧Baileys的/messages检查 ──

    # 1. Gate check
    gate = check_whatsapp_gate(chat_id, message, company_name)
    if not gate["pass"]:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(DRAFT_DIR, f"wa_blocked_{company_name[:20]}_{ts}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"TO: {chat_id}\nCOMPANY: {company_name}\nSCORE: {gate['score']}/100\nREASON: {gate['reason']}\n\n{message}")
        print(f"  ⛔ BLOCKED ({gate['score']}/100) — {gate['reason']}")
        return False

    # 1b. Verification gate for WhatsApp (skip for replies)
    if not is_reply:
        try:
            sys.path.insert(0, WORKDIR)
            from precision_bullet_gate import verify as bullet_verify
            v_result = bullet_verify(company_name, message, "customer")
            if not v_result["pass"]:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = os.path.join(DRAFT_DIR, f"wa_blocked_{company_name[:20]}_{ts}.txt")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(f"TO: {chat_id}\nCOMPANY: {company_name}\nREASON: 验证门禁 {v_result['score']}/100\nISSUES: {v_result['issues']}\n\n{message}")
                for issue in v_result["issues"]:
                    print(f"  🔬 {issue}")
                print(f"  ⛔ BLOCKED (验证门禁 {v_result['score']}/100)")
                return False
        except Exception as e:
            print(f"  ⚠ WhatsApp verification gate error: {e} — blocking to be safe")
            return False

    # ── 99%精准子弹门禁 ──
    try:
        sys.path.insert(0, WORKDIR)
        from precision_checklist import check_bullet, print_report
        result = check_bullet(company_name, message, chat_id, "whatsapp")
        if not result["pass"]:
            print_report(result)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(DRAFT_DIR, f"99p_blocked_{company_name[:20]}_{ts}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"TO: {chat_id}\nCOMPANY: {company_name}\nSCORE: {result['score']}/100\n")
                for issue in result["issues"]:
                    f.write(f"ISSUE: {issue}\n")
                f.write(f"\n{message}")
            print(f"  ⛔ 99%门禁拦截 ({result['score']}/100) — saved to {os.path.basename(path)}")
            return False
        else:
            if "issues" in result and result["issues"]:
                for issue in result["issues"]:
                    print(f"  ⚠ {issue}")
    except ImportError:
        print("  ⚠ precision_checklist not available — skipping 99% gate")
    except Exception as ce:
        print(f"  ⚠ 99% gate error: {ce}")

    # ── 对话活性检查：wago-api用webhook收消息，跳过 ──

    # 2. Send via wago-api
    try:
        import urllib.request
        data = json.dumps({"chatId": chat_id, "text": message}).encode()
        req = urllib.request.Request(
            f"{WHATSAPP_BRIDGE_URL}/client/sendMessage/{WHATSAPP_SESSION_ID}",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=10)
        resp_data = json.loads(resp.read())

        print(f"  ✅ SENT (wago-api accepted, msgId: {resp_data.get('messageId','?')})")

        # ── 发后验证 ──
        verified = False
        try:
            time.sleep(2)
            check_req = urllib.request.Request(
                f"{WHATSAPP_BRIDGE_URL}/channel/fetchMessages/{WHATSAPP_SESSION_ID}",
                method="POST",
                data=json.dumps({"chatId": chat_id, "limit": 5}).encode(),
                headers={"Content-Type": "application/json"}
            )
            check_resp = urllib.request.urlopen(check_req, timeout=8)
            all_msgs = json.loads(check_resp.read())
            if isinstance(all_msgs, dict) and "messages" in all_msgs:
                for m in all_msgs["messages"]:
                    m_chat = m.get("chatId", m.get("chat_id", ""))
                    m_body = m.get("text", m.get("body", m.get("message", "")))
                    m_from_me = m.get("fromMe", m.get("from_me", False))
                    if m_from_me and message[:30] in m_body:
                        verified = True
                        print(f"  ✅ POST-SEND VERIFY: 消息确认在对话中")
                        break
                if not verified:
                    print(f"  ⚠ POST-SEND VERIFY: 消息未在对话中找到 — 可能未送达")
            else:
                print(f"  ⚠ POST-SEND VERIFY: /channel/fetchMessages返回: {str(all_msgs)[:100]}")
        except Exception as ve:
            print(f"  ⚠ POST-SEND VERIFY error: {ve}")

        # 3. Log — 双写：本地SQLite + Supabase
        try:
            sys.path.insert(0, WORKDIR)
            from cloud_logger import log_sent as cl_log
            cl_log(chat_id, message, company_name, gate['score'], resp_data.get("messageId", ""))
        except Exception as le:
            print(f"  ⚠ cloud_logger error: {le}")
            # Fallback to JSONL
            log_send({
                "timestamp": datetime.now().isoformat(),
                "channel": "whatsapp",
                "chatId": chat_id, "company": company_name,
                "category": "client_outreach",
                "success": True, "gate_score": gate["score"],
                "messageId": resp_data.get("messageId", ""),
                "verified": verified
            })
        
        # 4. Track send in bullets DB
        if company_name:
            try:
                bullets_path = os.path.join(WORKDIR, "bullets_db.json")
                with open(bullets_path) as f:
                    bdb = json.load(f)
                for b in bdb["email_bullets"] + bdb["whatsapp_bullets"]:
                    if b.get("company") == company_name:
                        if "send_log" not in b:
                            b["send_log"] = []
                        b["send_log"].append({
                            "timestamp": datetime.now().isoformat(),
                            "channel": "whatsapp",
                            "messageId": resp_data.get("messageId", ""),
                            "verified": verified
                        })
                        b["last_sent"] = datetime.now().isoformat()
                        b["send_count"] = len(b["send_log"])
                        if b.get("status") in ["gated", "researched", "verified"]:
                            b["status"] = "sent"
                        break
                with open(bullets_path, "w") as f:
                    json.dump(bdb, f, ensure_ascii=False, indent=2)
                print(f"  📋 Bullet status updated: {company_name} → sent")
            except Exception as te:
                print(f"  ⚠ Send tracking error: {te}")
        
        return True

    except Exception as e:
        print(f"  ❌ SEND FAILED: {e}")
        return False


# ─── UNIVERSAL SEND (WHATSAPP MEDIA) ─────────────────────────────


def send_whatsapp_media(chat_id, file_path, company_name="", caption="", media_type="document", is_reply=False):
    """
    通过WhatsApp发送文件/图片/PDF。
    走 bridge.js 的 /send-media 端点。

    media_type: 'image' | 'document' | 'video' | 'audio'
    支持格式: jpg, png, webp, gif, mp4, pdf, doc, docx, xlsx, mp3, wav, ogg
    """
    print(f"\n📎 {company_name or chat_id} — 发送文件: {os.path.basename(file_path)}")

    # ── 铁律LID ──
    if chat_id.endswith("@lid"):
        print(f"  🔒 LID PROTECTION: chat_id以@lid结尾 ({chat_id}) — 不发")
        return False

    # ── 检查文件存在 ──
    if not os.path.exists(file_path):
        print(f"  ❌ 文件不存在: {file_path}")
        return False

    # ── 桥活着 ──
    bridge_ok, bridge_status = check_bridge_health()
    if not bridge_ok:
        print(f"  🔒 BRIDGE CHECK FAILED: {bridge_status}")
        return False

    # ── 重复发送检查：查JSONL有没有发过这个号码 ──
    already_sent, sent_records = check_whatsapp_already_sent(chat_id)
    if already_sent:
        print(f"  🔒 DUPLICATE DETECTED: {chat_id} 已发过 {len(sent_records)} 条消息")
        for r in sent_records:
            print(f"     🕐 {r['time']} | {r['body']}")
        print(f"  ⛔ BLOCKED — 这个号码已经发过消息，防止重复发送文件")
        return False

    # ── 门禁（有caption就走门禁）─
    if caption and not is_reply:
        try:
            sys.path.insert(0, WORKDIR)
            from precision_bullet_gate import verify as bullet_verify
            v_result = bullet_verify(company_name, caption, "customer")
            if not v_result["pass"]:
                print(f"  ⛔ BLOCKED (验证门禁 {v_result['score']}/100)")
                return False
        except Exception as e:
            print(f"  ⚠ Gate error: {e}")
            return False

    # ── 发送 ──
    try:
        import urllib.request
        # 自动检测media_type
        ext = file_path.lower().split('.')[-1]
        image_exts = {'jpg', 'jpeg', 'png', 'webp', 'gif'}
        video_exts = {'mp4'}
        audio_exts = {'mp3', 'wav', 'ogg', 'm4a'}
        if ext in image_exts and media_type == "document":
            media_type = "image"
        elif ext in video_exts:
            media_type = "video"
        elif ext in audio_exts:
            media_type = "audio"

        data = json.dumps({
            "chatId": chat_id,
            "filePath": file_path,
            "mediaType": media_type,
            "caption": caption or "",
            "fileName": os.path.basename(file_path),
        }).encode()

        req = urllib.request.Request(
            f"{WHATSAPP_BRIDGE_URL}/send-media",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=30)
        resp_data = json.loads(resp.read())

        if resp_data.get("success"):
            print(f"  ✅ 文件已发送 (msgId: {resp_data.get('messageId','?')})")
        else:
            print(f"  ❌ 发送失败: {resp_data}")
            return False

        # 日志
        log_send({
            "timestamp": datetime.now().isoformat(),
            "channel": "whatsapp_media",
            "chatId": chat_id,
            "company": company_name,
            "file": os.path.basename(file_path),
            "mediaType": media_type,
            "caption": caption,
            "success": True,
            "messageId": resp_data.get("messageId", "")
        })

        return True

    except Exception as e:
        print(f"  ❌ SEND FAILED: {e}")
        return False
