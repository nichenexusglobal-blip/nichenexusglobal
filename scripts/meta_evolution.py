

# ── HyperAgents Upgrade: Meta-improvement tracking ──

META_LOG = "C:/nichenexusglobal/meta_log.jsonl"

def log_correction_cycle(pen_correction, constraint_added, improvement_time_seconds):
    '''Track how fast I improve each cycle'''
    import json, os
    entry = {
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "correction": pen_correction,
        "constraint": constraint_added,
        "cycle_time_s": improvement_time_seconds,
        "cycle_type": "fast" if improvement_time_seconds < 30 else "slow"
    }
    with open(META_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    cycles = sum(1 for _ in open(META_LOG))
    print(f"  🔁 Correction cycle #{cycles}: {improvement_time_seconds}s → {entry['cycle_type']}")

def analyze_improvement_trend():
    '''Check if I'm getting faster at fixing errors'''
    import json, os
    if not os.path.exists(META_LOG):
        return "No data yet"
    times = []
    with open(META_LOG) as f:
        for line in f:
            try:
                entry = json.loads(line)
                times.append(entry.get("cycle_time_s", 0))
            except:
                pass
    if len(times) >= 3:
        avg_first3 = sum(times[:3]) / 3
        avg_last3 = sum(times[-3:]) / 3
        trend = "🔥 accelerating" if avg_last3 < avg_first3 else "⚡ stable" if avg_last3 == avg_first3 else "🐌 slowing"
        print(f"  📊 Meta-trend: {trend} (first 3: {avg_first3:.0f}s vs last 3: {avg_last3:.0f}s)")
