#!/usr/bin/env python3
import json

with open(r'C:\nichenexusglobal\.harness.json') as f:
    h = json.load(f)

print('=== Violation Records ===')
for v in h['violations']:
    print(f"  [{v['time']}] {v['file']}: {v['old_hash']} -> {v['new_hash']} ({v['status']})")

print()
print('=== Approved Changes ===')
for c in h['approved_changes']:
    print(f"  [{c['time']}] {c['file']}: {c['reason']}")
