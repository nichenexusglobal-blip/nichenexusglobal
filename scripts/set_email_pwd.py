#!/usr/bin/env python3
"""Set NICHE_EMAIL_PASSWORD env var from base64-encoded value."""
import base64, os, sys

encoded = "NGNkN3ZRNEdWNTlBVHh4dA=="
pwd = base64.b64decode(encoded).decode()
os.environ["NICHE_EMAIL_PASSWORD"] = pwd

# Write .env file at both locations
for path in [
    os.path.expanduser("~/nichenexusglobal/.env"),
    "D:/nichenexusglobal/.env"
]:
    with open(path, "w") as f:
        f.write(f"NICHE_EMAIL_PASSWORD={pwd}\n")
    print(f"Written: {path} ({len(pwd)} chars)")

print("Done. Password env var set and .env files written.")
