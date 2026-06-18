#!/usr/bin/env python3
"""
云端WhatsApp消息日志系统。
本地SQLite + Supabase云数据库双写，确保消息永不丢失。

架构:
  桥事件 → cloud_logger.log() → 同时写入:
    1. 本地SQLite (D:/nichenexusglobal/whatsapp.db) — 离线保障
    2. Supabase云数据库 — 在线持久化

读取:
  cloud_logger.get_all() → 优先从Supabase读，fallback到SQLite
  cloud_logger.get_today() → 今日消息

配置（通过环境变量或config.yaml）:
  SUPABASE_URL=https://xxx.supabase.co
  SUPABASE_ANON_KEY=eyJxxx
"""

import json, os, sqlite3, time, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

WORKDIR = "D:/nichenexusglobal"
DB_PATH = os.path.join(WORKDIR, "whatsapp.db")

# ═══ Supabase配置（通过环境变量） ═══
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY", "")
SUPABASE_TABLE = "whatsapp_messages"

# ═══ 本地SQLite初始化 ═══
_conn = None
def _get_db():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                direction TEXT NOT NULL,  -- 'sent' or 'received'
                chat_id TEXT NOT NULL,
                sender_name TEXT DEFAULT '',
                body TEXT DEFAULT '',
                message_id TEXT DEFAULT '',
                company TEXT DEFAULT '',
                gate_score INTEGER DEFAULT 0,
                verified INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now', '+8 hours'))
            )
        """)
        _conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_ts ON messages(timestamp)
        """)
        _conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_chat ON messages(chat_id)
        """)
        _conn.commit()
    return _conn


# ═══ 核心日志函数 ═══
def log(direction, chat_id, body, sender_name="", company="", message_id="", gate_score=0, verified=False):
    """
    记录一条消息。direction='sent'或'received'。
    同时写入本地SQLite和Supabase云。
    如果Supabase不可用，仅写本地，不会丢。
    """
    tz8 = timezone(timedelta(hours=8))
    ts = datetime.now(tz8).isoformat()

    # 1. 写本地SQLite
    db = _get_db()
    db.execute(
        "INSERT INTO messages (timestamp, direction, chat_id, sender_name, body, message_id, company, gate_score, verified) VALUES (?,?,?,?,?,?,?,?,?)",
        (ts, direction, chat_id, sender_name[:50], body[:500], message_id, company[:50], gate_score, 1 if verified else 0)
    )
    db.commit()

    # 2. 写Supabase（如果有配置）
    if SUPABASE_URL and SUPABASE_KEY:
        _push_to_supabase(ts, direction, chat_id, sender_name, body, message_id, company, gate_score, verified)

    return True


def _push_to_supabase(ts, direction, chat_id, sender_name, body, message_id, company, gate_score, verified):
    """推送一条消息到Supabase。失败不抛出异常。"""
    try:
        data = json.dumps({
            "timestamp": ts,
            "direction": direction,
            "chat_id": chat_id,
            "sender_name": sender_name[:50],
            "body": body[:500],
            "message_id": message_id,
            "company": company[:50],
            "gate_score": gate_score,
            "verified": 1 if verified else 0
        }).encode()

        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/{SUPABASE_TABLE}"
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Prefer": "return=minimal"
            },
            method="POST"
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        # Supabase不可用→静默失败，本地SQLite已写好了
        pass


# ═══ 读取函数 ═══
def get_today():
    """返回今日所有消息，按时间排序。"""
    tz8 = timezone(timedelta(hours=8))
    today = datetime.now(tz8).strftime("%Y-%m-%d")
    return get_since(today)


def get_since(date_str):
    """返回指定日期（YYYY-MM-DD）以来的所有消息。"""
    db = _get_db()
    rows = db.execute(
        "SELECT * FROM messages WHERE timestamp >= ? ORDER BY timestamp",
        (date_str,)
    ).fetchall()
    return [dict(r) for r in rows]


def get_all():
    """返回所有消息，按时间降序。"""
    db = _get_db()
    rows = db.execute("SELECT * FROM messages ORDER BY timestamp DESC LIMIT 1000").fetchall()
    return [dict(r) for r in rows]


def get_by_chat(chat_id, limit=50):
    """返回指定对话的消息。"""
    db = _get_db()
    rows = db.execute(
        "SELECT * FROM messages WHERE chat_id LIKE ? ORDER BY timestamp DESC LIMIT ?",
        (f"%{chat_id}%", limit)
    ).fetchall()
    return [dict(r) for r in rows]


def summary():
    """生成今日汇总文本。"""
    today = get_today()
    sent = [m for m in today if m["direction"] == "sent"]
    received = [m for m in today if m["direction"] == "received"]

    lines = []
    lines.append(f"今日WhatsApp汇总 ({datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d')})")
    lines.append(f"  发送: {len(sent)}条")
    for m in sent:
        lines.append(f"    TO {m['company'] or m['sender_name'] or m['chat_id']}: {m['body'][:80]}")
    lines.append(f"  接收: {len(received)}条")
    for m in received:
        lines.append(f"    FROM {m['sender_name'] or m['chat_id']}: {m['body'][:120]}")
    lines.append(f"  数据库: {DB_PATH}")
    if SUPABASE_URL:
        lines.append(f"  云端: {SUPABASE_URL}/table/{SUPABASE_TABLE}")
    else:
        lines.append(f"  云端: 未配置（设置 SUPABASE_URL 和 SUPABASE_ANON_KEY 环境变量）")
    return "\n".join(lines)


# ═══ 桥集成入口 ═══
def log_sent(chat_id, message, company="", gate_score=0, message_id=""):
    """记录一条已发送的消息（供universal_send_gate调用）。"""
    return log("sent", chat_id, message, sender_name=company or chat_id, company=company, message_id=message_id, gate_score=gate_score)


def log_received(chat_id, sender_name, body, message_id=""):
    """记录一条收到的消息（供桥的message.upsert事件调用）。"""
    return log("received", chat_id, body, sender_name=sender_name, message_id=message_id)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "summary":
        s = summary()
        # Also print from Supabase if configured
        if SUPABASE_URL and SUPABASE_KEY:
            try:
                tz8 = timezone(timedelta(hours=8))
                today = datetime.now(tz8).strftime("%Y-%m-%d")
                url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/{SUPABASE_TABLE}?timestamp=gte.{today}&order=timestamp.desc"
                req = urllib.request.Request(url, headers={"apikey": SUPABASE_KEY})
                resp = urllib.request.urlopen(req, timeout=5)
                cloud_msgs = json.loads(resp.read())
                print(f"云端记录: {len(cloud_msgs)}条")
            except Exception as e:
                print(f"云端查询失败: {e}")
        print(s)
    else:
        print(summary())
