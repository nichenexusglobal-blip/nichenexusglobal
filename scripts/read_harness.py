#!/usr/bin/env python3
"""Read harness.json for daily review"""
import json

with open('/c/nichenexusglobal/.harness.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("Last approved:", d.get('last_approved', 'N/A'))
print("\nViolations count:", len(d.get('violations', [])))
for v in d.get('violations', [])[:10]:
    print(f"  - {v.get('file','')} : {v.get('reason','')} : {v.get('time','')}")
print("\nPending approvals count:", len(d.get('pending_approvals', [])))
for p in d.get('pending_approvals', [])[:5]:
    print(f"  - {p.get('file','')} : {p.get('reason','')}")
