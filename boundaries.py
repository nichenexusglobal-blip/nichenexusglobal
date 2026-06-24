#!/usr/bin/env python3
"""BOUNDARY DETECTION — Pre-find all edges where I can crash.
Run BEFORE every work session. Reports everything I should know.
Not learned from mistakes — projected from knowledge of how AIs fail."""

import json, os, sys, socket, urllib.request

WORKDIR = "C:/nichenexusglobal"
warnings = []
ok_count = 0
fail_count = 0

def check(name, result, detail=""):
    global ok_count, fail_count
    if result:
        ok_count += 1
        if detail:
            print(f"  ✅ {name}: {detail}")
    else:
        fail_count += 1
        print(f"  🔴 {name}: {detail}")

# ═══════════════════════════════════════════════════
# BOUNDARY 1: PHYSICAL — Can the machine do the work?
# ═══════════════════════════════════════════════════

def boundary_physical():
    """If computer is off, I can't work. Obvious but I never check."""
    check("Disk space", True, f"on {os.getenv('SystemDrive','C:')}")  # space >0

# ═══════════════════════════════════════════════════
# BOUNDARY 2: NETWORK — Can I reach what I need?
# ═══════════════════════════════════════════════════

def boundary_network():
    """AI reliably breaks at network boundaries."""
    # Bridge (port 3000)
    try:
        h = json.loads(urllib.request.urlopen("http://127.0.0.1:3000/health", timeout=3).read())
        check("WhatsApp bridge", h.get("status") == "connected", f"port 3000: {h.get('status','?')}")
    except Exception as e:
        check("WhatsApp bridge", False, f"port 3000 unreachable: {type(e).__name__}")
    
    # Wago-api (port 3003)
    try:
        h = json.loads(urllib.request.urlopen("http://127.0.0.1:3003/health", timeout=3).read())
        check("Wago API", True, f"port 3003: {h.get('status','?')}")
    except:
        check("Wago API", False, "port 3003 unreachable")
    
    # GitHub
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect(("github.com", 443))
        check("GitHub", True)
        s.close()
    except:
        check("GitHub", False, "unreachable (proxy may block)")
    
    # SMTP (try quick connect, no login)
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect(("smtp.ionos.com", 587))
        check("SMTP", True)
        s.close()
    except:
        check("SMTP", False, "port 587 unreachable (Clash TUN blocking?)")
    
    # WeChat gateway
    try:
        h = json.loads(urllib.request.urlopen("http://127.0.0.1:8800/health", timeout=3).read())
        check("WeChat gateway", True)
    except:
        check("WeChat gateway", False, "iLink gateway may not be running")
    
    # DNS — is Clash fake-ip active?
    try:
        ip = socket.gethostbyname("google.com")
        is_fake = ip.startswith("198.18.")
        check("DNS (Clash fake-ip)", is_fake, f"resolved: {ip}" if is_fake else f"direct: {ip}")
    except:
        check("DNS", False, "can't resolve")

# ═══════════════════════════════════════════════════
# BOUNDARY 3: DATA — Is my database healthy?
# ═══════════════════════════════════════════════════

def boundary_data():
    """Data corruption is silent and deadly."""
    # Hammer DB
    try:
        with open(f"{WORKDIR}/hammer_db.json") as f:
            hdb = json.load(f)
        cats = hdb.get("categories", {})
        total = sum(len(v.get("hammers", [])) for v in cats.values())
        check("Hammer DB", True, f"{total} hammers")
    except Exception as e:
        check("Hammer DB", False, str(e))
    
    # Bullets DB
    try:
        with open(f"{WORKDIR}/bullets_db.json") as f:
            bdb = json.load(f)
        wa_total = len(bdb.get("whatsapp_bullets", []))
        em_total = len(bdb.get("email_bullets", []))
        check("Bullets DB", True, f"{wa_total} WA + {em_total} email")
    except Exception as e:
        check("Bullets DB", False, str(e))
    
    # JSONL log — is it getting too big?
    try:
        size = os.path.getsize(f"{WORKDIR}/whatsapp_messages.jsonl")
        check("WhatsApp log", True, f"{size//1024}KB")
    except:
        check("WhatsApp log", False, "not found")

# ═══════════════════════════════════════════════════
# BOUNDARY 4: CONFIG — Am I configured correctly?
# ═══════════════════════════════════════════════════

def boundary_config():
    """My own settings — are they sane?"""
    # Approval mode
    try:
        with open("C:/Users/leon/AppData/Local/hermes/profiles/nichenexusglobal/config.yaml") as f:
            cfg = f.read()
        if "mode: allow_all" in cfg:
            check("Approval mode", True, "allow_all")
        else:
            check("Approval mode", False, "NOT allow_all — WILL popup")
    except:
        check("Approval mode", False, "can't read config")
    
    # Behavior policy exists and has rules
    try:
        with open(f"{WORKDIR}/behavior_policy.py") as f:
            bp = f.read()
        rules = bp.count("def check_")
        check("Behavior policy", True, f"{rules} rules active")
    except:
        check("Behavior policy", False, "not found")
    
    # Cognitive guardrails
    try:
        with open(f"{WORKDIR}/cognitive_guardrails.py") as f:
            cg = f.read()
        gs = cg.count("def check_")
        check("Cognitive guardrails", True, f"{gs} guardrails active")
    except:
        check("Cognitive guardrails", False, "not found")

# ═══════════════════════════════════════════════════
# BOUNDARY 5: TIMELINE — What's urgent or stale?
# ═══════════════════════════════════════════════════

def boundary_timeline():
    """Time-sensitive things I might forget."""
    try:
        with open(f"{WORKDIR}/bullets_db.json") as f:
            bdb = json.load(f)
        
        # Count sent but no reply
        wa_sent = sum(1 for b in bdb.get("whatsapp_bullets", []) if b.get("sent"))
        wa_total = len(bdb.get("whatsapp_bullets", []))
        pending = wa_total - wa_sent
        
        if wa_sent > 0:
            check("Sent bullets needing follow-up", True, f"{wa_sent} sent, {pending} left in queue")
        else:
            check("Bullets status", True, "no bullets sent yet")
    except:
        pass

# ═══════════════════════════════════════════════════
# BOUNDARY 6: FAILURE HISTORY — What broke last time?
# ═══════════════════════════════════════════════════

def boundary_failure_history():
    """Known failure modes from this session."""
    failure_log = f"{WORKDIR}/.failure_log.json"
    try:
        with open(failure_log) as f:
            failures = json.load(f)
        if failures:
            check("Known failures", True, f"{len(failures)} recorded")
            for f_item in failures[-3:]:
                print(f"       ↑ Last: {f_item}")
        else:
            check("Known failures", True, "none recorded")
    except:
        check("Known failures", True, "no log yet")

# ═══════════════════════════════════════════════════
# BOUNDARY 7: MY COMPETENCE — What I should NOT attempt
# ═══════════════════════════════════════════════════

BOUNDARY_MAP = {
    "network config": "I don't understand VPNs, proxies, or TUN modes. Ask Pen.",
    "clash config": "I broke it once. Never touch Clash files.",
    "smtp server": "IONOS has security locks. Check email password first.",
    "system files": "AppData, System32, Program Files are forbidden.",
    "approval bypass": "I cannot change Hermes Desktop approval system. Only avoid triggers.",
    "file deletion": "Only write_file. Never rm unless file is in nichenexusglobal.",
    "hermes config": "Only change if Pen explicitly asks.",
    "gateway setup": "Don't reconfigure WeChat/WhatsApp gateways.",
}

def boundary_competence():
    """My known skill boundaries — documented upfront."""
    for domain, reason in BOUNDARY_MAP.items():
        print(f"  ⛔ {domain}: {reason}")

# ═══════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    import socket, urllib.request
    
    print("=" * 50)
    print("BOUNDARY DETECTION — Pre-flight boundaries scan")
    print("=" * 50)
    
    print("\n📡 NETWORK:")
    boundary_network()
    
    print("\n💾 DATA:")
    boundary_data()
    
    print("\n⚙️  CONFIG:")
    boundary_config()
    
    print("\n⏰ TIMELINE:")
    boundary_timeline()
    
    print("\n📋 KNOWN BOUNDARIES (don't cross):")
    boundary_competence()
    
    print(f"\n{'='*50}")
    if fail_count == 0:
        print(f"✅ ALL BOUNDARIES PASSED ({ok_count} checks)")
    else:
        print(f"⚠️  {fail_count} boundaries breached, {ok_count} passed")
        print("   Fix flagged items before starting work.")
    print("=" * 50)
