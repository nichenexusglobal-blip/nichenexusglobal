#!/usr/bin/env python3
"""
WhatsApp消息云归档器。
每300秒轮询桥的/messages端点，将收到的消息写入cloud_logger（本地SQLite+Supabase双写）。
取代旧的JSONL归档器。
注意：轮询频率已从15秒降低到300秒以减少磁盘IO。cron看门狗已经覆盖实时性需求。"""
import json, os, sys, time, urllib.request

WORKDIR = "D:/nichenexusglobal"
BRIDGE_URL = "http://127.0.0.1:3000"
POLL_INTERVAL = 300  # 秒（5分钟，从15秒降低以减少磁盘IO）
SEEN_FILE = os.path.join(WORKDIR, ".cloud_archiver_seen.json")

sys.path.insert(0, WORKDIR)
from cloud_logger import log_received

def load_seen():
    try:
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(ids):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(ids), f)

def poll():
    seen = load_seen()
    while True:
        try:
            req = urllib.request.Request(f"{BRIDGE_URL}/messages", method="GET")
            resp = urllib.request.urlopen(req, timeout=8)
            msgs = json.loads(resp.read())
            if isinstance(msgs, list):
                for m in msgs:
                    msg_id = m.get("message_id", m.get("id", ""))
                    from_me = m.get("from_me", m.get("fromMe", False))
                    # 只记录收到的消息（发送的消息由universal_send_gate记录）
                    if not from_me and msg_id and msg_id not in seen:
                        log_received(
                            chat_id=m.get("chat_id", m.get("chatId", "")),
                            sender_name=m.get("sender_name", ""),
                            body=m.get("body", ""),
                            message_id=msg_id
                        )
                        seen.add(msg_id)
                        print(f"[{time.strftime('%H:%M:%S')}] 归档: {m.get('sender_name','?')}: {m.get('body','')[:60]}")
                save_seen(seen)
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] 轮询错误: {e}")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    print(f"🔵 WhatsApp云归档器启动 - 每{POLL_INTERVAL}秒轮询")
    print(f"   本地: {WORKDIR}/whatsapp.db")
    print(f"   云端: 需配置SUPABASE_URL环境变量")
    print(f"   去重文件: {SEEN_FILE}")
    try:
        poll()
    except KeyboardInterrupt:
        print("\n停止")
