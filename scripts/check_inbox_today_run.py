#!/usr/bin/env python3
"""Quick wrapper that sets pwd env and checks inbox."""
import base64, os, sys, time
os.environ["NICHE_EMAIL_PASSWORD"] = base64.b64decode("NGNkN3ZRNEdWNTlBVHh4dA==").decode()
print(f"PWD set, length={len(os.environ['NICHE_EMAIL_PASSWORD'])}", flush=True)
# Run the actual checker
sys.argv = ['check_inbox_today.py']
exec(open(os.path.join(os.path.dirname(__file__), "check_inbox_today.py"), encoding="utf-8").read())
