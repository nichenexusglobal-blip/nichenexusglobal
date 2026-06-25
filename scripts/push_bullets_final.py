#!/usr/bin/env python
"""GitHub push with curl API"""
import json, base64, sys, os, urllib.request

env_path = r'C:\nichenexusglobal\.env'
token = None
with open(env_path, 'r') as f:
    for rawline in f:
        rawline = rawline.strip()
        if rawline.startswith('GIT_TOKEN=***                token = rawline.split('=', 1)[1].strip().strip("'\"")
                break
if not token:
    print("FAIL: No GIT_TOKEN")
    sys.exit(1)

with open(r'C:\nichenexusglobal\bullets_db.json', 'r', encoding='utf-8') as f:
    content = f.read()

url = "https://api.github.com/repos/l294723699/nichenexusglobal/contents/bullets_db.json"
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"})
resp = json.loads(urllib.request.urlopen(req, timeout=15).read().decode())
sha = resp['sha']
print(f"Current SHA: {sha}")

encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
payload = {
    "message": "bullets_db: clear email bullet library - sent 8 new emails June 25",
    "content": encoded,
    "sha": sha,
    "branch": "main"
}
req2 = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'),
    headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"},
    method="PUT")
result = json.loads(urllib.request.urlopen(req2, timeout=15).read().decode())
print(f"PUSHED: {result.get('commit', {}).get('sha', 'unknown')}")
