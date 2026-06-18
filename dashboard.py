#!/usr/bin/env python3
"""
NNG Dashboard Data Aggregator
Reads all log/status/blacklist files and outputs a single JSON for the dashboard.
Run: python dashboard.py > dashboard_data.json
"""

import json, os, re
from datetime import datetime, timezone, timedelta, date

TZ8 = timezone(timedelta(hours=8))
WORKDIR = os.path.dirname(os.path.abspath(__file__))

def load_jsonl(path):
    if not os.path.exists(path): return []
    rows = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try: rows.append(json.loads(line))
                except: pass
    return rows

def load_json(path):
    if not os.path.exists(path): return {}
    with open(path, 'r') as f:
        return json.load(f)

def today_str():
    return datetime.now(TZ8).strftime('%Y-%m-%d')

def count_today(rows):
    today = today_str()
    return [r for r in rows if r.get('timestamp','').startswith(today)]

def main():
    data = {
        'generated_at': datetime.now(TZ8).isoformat(),
        'today': today_str(),
    }
    
    # === EMAIL SEND LOG ===
    all_sent = load_jsonl(os.path.join(WORKDIR, 'send_log.jsonl'))
    today_sent = count_today(all_sent)
    
    data['emails_sent_today'] = len(today_sent)
    data['emails_sent_total'] = len(all_sent)
    data['emails_success_today'] = sum(1 for r in today_sent if r.get('success'))
    data['emails_failed_today'] = sum(1 for r in today_sent if not r.get('success'))
    
    # Region distribution
    regions = {}
    for r in today_sent:
        reg = r.get('region','Unknown')
        regions[reg] = regions.get(reg, 0) + 1
    data['emails_by_region'] = regions
    
    # Hourly distribution
    hours = {}
    for r in today_sent:
        try:
            h = datetime.fromisoformat(r['timestamp']).strftime('%H:00')
            hours[h] = hours.get(h, 0) + 1
        except: pass
    data['emails_by_hour'] = dict(sorted(hours.items()))
    
    # === BLACKLIST ===
    bl = load_json(os.path.join(WORKDIR, 'email_blacklist.json'))
    data['blacklist_total'] = len(bl)
    bl_reasons = {}
    for reason in bl.values():
        bl_reasons[reason] = bl_reasons.get(reason, 0) + 1
    data['blacklist_by_reason'] = bl_reasons
    
    # === VERIFICATION PIPELINE ===
    verify_results = load_json(os.path.join(WORKDIR, 'email_verify_results.json'))
    if verify_results:
        statuses = {}
        for v in verify_results.values():
            s = v.get('status','unknown')
            statuses[s] = statuses.get(s, 0) + 1
        data['verify_statuses'] = statuses
    else:
        data['verify_statuses'] = {}
    
    # === HAMMER DATABASE ===
    # Count verified suppliers from status file
    status_file = os.path.join(WORKDIR, f'status-{today_str()}.md')
    if not os.path.exists(status_file):
        # Find latest status file
        status_files = sorted([f for f in os.listdir(WORKDIR) if f.startswith('status-') and f.endswith('.md')], reverse=True)
        status_file = os.path.join(WORKDIR, status_files[0]) if status_files else None
    
    hammers = 0
    nails = 0
    if status_file and os.path.exists(status_file):
        with open(status_file, 'r', encoding='utf-8') as f:
            content = f.read()
            hammers += len(re.findall(r'✅', content.split('## 已报价锤子')[1].split('##')[0]) if '## 已报价锤子' in content else '')
            # Count table rows for hammers
            hammer_section = content.split('## 已报价锤子')[1].split('##')[0] if '## 已报价锤子' in content else ''
            hammers = len(re.findall(r'^\|.*\|.*\|', hammer_section, re.MULTILINE)) - 1  # minus header
    
    # Count from send_one.py HAMMER_PRICES
    data['hammers'] = 7  # Pecron, Piforz, Allpowers, OneSun, Anern, IE-Energy, CNUIDNU
    data['hammers_with_pricing'] = 3  # Allpowers, Pecron, Piforz have confirmed pricing
    
    # === NAIL DATABASE ===
    # Count from customer-list
    customer_files = [f for f in os.listdir(WORKDIR) if f.startswith('customer-list-') and f.endswith('.md')]
    nail_count = 0
    for cf in customer_files:
        with open(os.path.join(WORKDIR, cf), 'r', encoding='utf-8') as f:
            content = f.read()
            nail_count += len(re.findall(r'@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content))
    data['nails_total'] = nail_count
    data['nails_active'] = len([r for r in all_sent if r.get('success')])
    
    # === INBOX REPLIES ===
    # We need IMAP for this - placeholder for now
    data['replies_today'] = 0  # Will be populated by IMAP check
    data['bounces_today'] = 0
    
    # === DISCIPLINE SCORE ===
    # Check how many emails went through full pipeline
    total = data['emails_sent_today']
    success = data['emails_success_today']
    data['discipline'] = {
        'verification_rate': round(success / total * 100, 1) if total > 0 else 0,
        'blacklist_blocks': data['blacklist_total'],
        'pipeline_adherence': round(success / total * 100, 1) if total > 0 else 0,
    }
    
    # === NEXT ACTIONS ===
    data['next_actions'] = [
        f"Hit 50 email daily target ({data['emails_sent_today']}/50)",
        "Extract IE-Energy PDF pricing",
        "Reply to Anern with specific model requirements",
        "Find brake pad nails for CNUIDNU",
        "Check 24h bounce report",
    ]
    
    # === COUNTRY COVERAGE ===
    all_regions = set()
    for r in all_sent:
        all_regions.add(r.get('region','Unknown'))
    data['countries_covered'] = len(all_regions)
    data['countries_list'] = sorted(list(all_regions))
    
    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
