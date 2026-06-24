#!/usr/bin/env python3
"""BEHAVIOR POLICY — Full human cognition guardrails
Every pattern that makes humans reliable vs AI brittle.
Encoded as permanent checks."""
import sys, os, json, time

WORKDIR = "C:/nichenexusglobal"
errors = []
warnings = []

# ═══════════════════════════════════════════════════
# COGNITIVE GUARDRAIL 1: 3-STRIKES RULE
# Any operation that fails 3 times → STOP. Escalate.
# ═══════════════════════════════════════════════════

STRIKES = {}  # operation_id → strike_count

def check_three_strikes(op_id):
    """If same operation failed 3+ times, block it."""
    STRIKES[op_id] = STRIKES.get(op_id, 0) + 1
    if STRIKES[op_id] >= 3:
        errors.append(f"🧠 CG1: '{op_id}' failed {STRIKES[op_id]} times. STOP. Escalate to Pen.")
    return STRIKES[op_id]

# ═══════════════════════════════════════════════════
# COGNITIVE GUARDRAIL 2: KNOW-WHAT-YOU-KNOW CHECK
# Never claim something from guessing.
# ═══════════════════════════════════════════════════

UNSAFE_PATTERNS = [
    "probably", "likely", "should work", "must be", "I think",
    "I believe", "probably just", "should be fine", "in theory",
    "you could try", "maybe", "might be", "possibly"
]

def check_guesswork(text):
    """Flag when I'm using guesswork language."""
    text_lower = text.lower()
    for pattern in UNSAFE_PATTERNS:
        if pattern in text_lower:
            warnings.append(f"🧠 CG2: '{pattern}' in output — am I guessing? Verify first.")
            break

# ═══════════════════════════════════════════════════
# COGNITIVE GUARDRAIL 3: CONTEXT-CHANGE CHECK
# Environment may have changed since last successful operation.
# ═══════════════════════════════════════════════════

CONTEXT_FILE = f"{WORKDIR}/.context_snapshot.json"

def check_context_stable():
    """Check if things that worked before still work."""
    try:
        with open(CONTEXT_FILE) as f:
            prev = json.load(f)
    except:
        # First run — save snapshot
        save_context()
        return
    
    curr = get_context()
    for key, val in prev.items():
        if curr.get(key) != val:
            warnings.append(f"🧠 CG3: Context changed: {key} was {val}, now {curr.get(key)}")

def get_context():
    """Snapshot key environment variables."""
    ctx = {}
    # Check if bridge is running
    try:
        import urllib.request
        h = json.loads(urllib.request.urlopen("http://127.0.0.1:3000/health", timeout=2).read())
        ctx["bridge"] = h.get("status", "unknown")
    except:
        ctx["bridge"] = "offline"
    # Check GitHub reachability
    import socket
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect(("github.com", 443))
        ctx["github"] = "reachable"
        s.close()
    except:
        ctx["github"] = "unreachable"
    return ctx

def save_context():
    os.makedirs(WORKDIR, exist_ok=True)
    with open(CONTEXT_FILE, "w") as f:
        json.dump(get_context(), f)

# ═══════════════════════════════════════════════════
# COGNITIVE GUARDRAIL 4: VERIFICATION LOOP
# After every write → read back and verify.
# ═══════════════════════════════════════════════════

def check_data_written(filepath):
    """Verify a file was written correctly."""
    try:
        if not os.path.exists(filepath):
            errors.append(f"🧠 CG4: File {filepath} doesn't exist after write!")
            return
        size = os.path.getsize(filepath)
        if size == 0:
            errors.append(f"🧠 CG4: File {filepath} is empty after write!")
            return
        # JSON files should parse
        if filepath.endswith(".json"):
            with open(filepath) as f:
                json.load(f)
    except json.JSONDecodeError:
        errors.append(f"🧠 CG4: {filepath} is invalid JSON after write!")
    except Exception as e:
        errors.append(f"🧠 CG4: {filepath} verify failed: {e}")

# ═══════════════════════════════════════════════════
# COGNITIVE GUARDRAIL 5: QUALIFICATION CHECK
# Don't touch systems I don't understand.
# ═══════════════════════════════════════════════════

BLOCKED_SYSTEMS = [
    "clash", "clash-verge", "Merge.yaml", "mihomo",
    "firewall", "network adapter", "dns config",
    "system proxy", "tun mode", "fake-ip",
    "registry", "group policy"
]

def check_qualification(text):
    """If the task involves systems I don't understand, flag it."""
    text_lower = text.lower()
    for sys_name in BLOCKED_SYSTEMS:
        if sys_name in text_lower:
            warnings.append(f"🧠 CG5: '{sys_name}' — I don't fully understand this system. Ask Pen before modifying.")
            break

# ═══════════════════════════════════════════════════
# COGNITIVE GUARDRAIL 6: CHECK THE SIMPLE THINGS FIRST
# Before debugging complex issues, verify fundamentals.
# ═══════════════════════════════════════════════════

def check_fundamentals_first(task):
    """For common failure modes, check simple causes first."""
    if "smtp" in task or "email" in task:
        # Check if password file exists before blaming proxy
        try:
            with open("C:/Users/leon/AppData/Local/hermes/profiles/nichenexusglobal/.env") as f:
                for line in f:
                    if "EMAIL_PASSWORD" in line and "=" in line:
                        pwd = line.split("=", 1)[1].strip()
                        if len(pwd) < 8:
                            errors.append("🧠 CG6: EMAIL_PASSWORD seems too short — check if .env is corrupted")
                        break
        except:
            warnings.append("🧠 CG6: Can't read .env — password may be missing")

# ═══════════════════════════════════════════════════
# COGNITIVE GUARDRAIL 7: ESCALATION THRESHOLD
# Know when to ask Pen vs keep trying.
# ═══════════════════════════════════════════════════

def check_escalation_needed(attempt_count, task_name):
    """After N failed attempts, escalate."""
    if attempt_count >= 3:
        errors.append(f"🧠 CG7: Tried {task_name} {attempt_count} times with no success. Need Pen's input.")

# ═══════════════════════════════════════════════════
# COGNITIVE GUARDRAIL 8: BULLET TRUTH CHECK
# Every claim about a customer must trace to a real page visit.
# ═══════════════════════════════════════════════════

def check_bullet_truth(bullet_text):
    """Flag any bullet with claims I haven't personally verified."""
    import re
    
    # Red flags — claims that need verification from the customer's own site
    claims = re.findall(
        r"I see you[^.]*\.|I notice[^.]*\.|you sell[^.]*\.|"
        r"you carry[^.]*\.|you offer[^.]*\.|you distribute[^.]*\.|"
        r"you stock[^.]*\.|you import[^.]*\.|your website shows[^.]*\.",
        bullet_text, re.IGNORECASE
    )
    
    if claims:
        warnings.append(f"🧠 CG8: {len(claims)} claims about customer in bullet:")
        for c in claims[:3]:
            short = c.strip()[:60]
            warnings.append(f"       → '{short}' — verify from customer's website, not search snippet")
    
    # Check for numbers without sources
    prices = re.findall(r'[£$€]\s*[\d,]+', bullet_text)
    if prices:
        warnings.append(f"🧠 CG8: {len(prices)} price mention(s): verify from quotation or customer site")

# ═══════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════

def run_all_checks(task="", text="", attempt=0, task_name="", bullet_text=""):
    """Run all cognitive guardrails."""
    check_guesswork(text)
    check_qualification(text)
    check_fundamentals_first(task)
    if bullet_text:
        check_bullet_truth(bullet_text)
    if attempt > 0 and task_name:
        check_escalation_needed(attempt, task_name)
    return errors, warnings

if __name__ == "__main__":
    import sys, json
    args = sys.argv[1:]
    task = " ".join(args) if args else ""
    
    errs, warns = run_all_checks(task=task)
    
    if errs or warns:
        if warnings:
            for w in warns:
                print(f"  ⚠️  {w}")
        if errors:
            for e in errors:
                print(f"  🔴 {e}")
            sys.exit(1)
        else:
            print("✅ Cognitive checks passed (with warnings)")
    else:
        print("✅ Cognitive guardrails: all clear")
