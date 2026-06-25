#!/usr/bin/env python
"""GitHub push using simple token reading"""
import json, base64, urllib.request, os

# Read env line by line
env_path = r'C:\nichenexusglobal\.env'
git_token = None
with open(env_path, 'r') as fh:
    for raw in fh:
        raw = raw.strip()
        if 'GIT_TOKEN=' in raw:
            parts = raw.split('=', 1)
            if len(parts) == 2:
                git_token = parts[1].strip().strip("'\\\"")
            break

if not git_token:
    print("FAIL: No GIT_TOKEN found")
    exit(1)

with open(r'C:\nichenexusglobal\bullets_db.json', 'r', encoding='utf-8') as f:
    content = f.read()

url = "https://api.github.com/repos/l294723699/nichenexusglobal/contents/bullets_db.json"
req = urllib.request.Request(url,
    headers={"Authorization": f"Bearer {git_token}", "Accept": "application/vnd.github.v3+json"})
resp = json.loads(urllib.request.urlopen(req, timeout=15).read().decode())
sha = resp['sha']
print(f"SHA: {sha}")

encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
payload = json.dumps({
    "message": "bullets_db: clear email bullet library - sent 8 new emails June 25",
    "content": encoded,
    "sha": sha,
    "branch": "main"
}).encode('utf-8')

req2 = urllib.request.Request(url, data=payload,
    headers={"Authorization": f"Bearer {git_token}", "Accept": "application/vnd.github.v3+json"},
    method="PUT")
result = json.loads(urllib.request.urlopen(req2, timeout=15).read().decode())
print(f"PUSHED: {result.get('commit', {}).get('sha', 'unknown')}")
