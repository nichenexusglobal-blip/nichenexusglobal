#!/usr/bin/env python3
"""Read harness from correct path"""
import json, os

# Try multiple paths
for path in ['/c/nichenexusglobal/.harness.json', 
             'C:/nichenexusglobal/.harness.json',
             os.path.expanduser('~/.hermes/profiles/nichenexusglobal/.harness.json')]:
    if os.path.exists(path):
        print(f"Found at: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            d = json.load(f)
        print("Last approved:", d.get('last_approved', 'N/A'))
        violations = d.get('violations', [])
        print(f"Violations: {len(violations)}")
        for v in violations:
            print(f"  - {v.get('file','')} : {v.get('reason','')} : {v.get('time','')}")
        pending = d.get('pending_approvals', [])
        print(f"Pending approvals: {len(pending)}")
        for p in pending:
            print(f"  - {json.dumps(p, ensure_ascii=False)[:200]}")
        break
else:
    print("HARNESS_NOT_FOUND")
